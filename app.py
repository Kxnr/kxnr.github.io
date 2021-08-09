import os
import itsdangerous

# flask and extensions
from flask import Flask, url_for, g, send_from_directory, request
from flask_security import auth_required, Security, roles_accepted, current_user, logout_user
from flask_minify import minify

# internal to this app
import components
from forms import ExtendedLoginForm, username_mapper, ExtendedTwoFactorSetupForm, ExtendedRegisterForm
from models import db
from pykxnr.config import Config, load_configuration
from cli import content, category, server
from datastore import create_user_datastore, create_content_datastore
from utils import decrypt_resource
import pages
import components


app = Flask(__name__)

##########
# Configuration
##########
minify(app=app, html=True, js=True, cssless=True)
app.cli.add_command(content, "content")
app.cli.add_command(category, "category")
app.cli.add_command(server, "server")

app.jinja_env.add_extension('jinja2.ext.do')

def split_space(string):
    return string.strip().split()

app.jinja_env.filters['split_space'] = split_space

# Load configuration from file
config_file = os.environ["FLASK_CONFIG"]
load_configuration(config_file)
app.config.update(Config.common.freeze())

if app.config["ENV"] == "production":
    app.config.update(Config.production.freeze())
else:
    app.config.update(Config.development.freeze())

# Configuration options that rely on running python
app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = [{"username": {"mapper": username_mapper}}]
app.config["render_format"] =  {"article": components.Article,
                                "gallery": components.Panels,
                                "pdf": components.Pdf,
                                "full_header": components.FullHeader}

##########
# Initialization
##########
db.init_app(app)
security = Security(app, create_user_datastore(), login_form=ExtendedLoginForm,
                    two_factor_setup_form=ExtendedTwoFactorSetupForm,
                    confirm_register_form=ExtendedRegisterForm)

content_datastore = create_content_datastore()

##########
# Exception/Error handling
##########

@app.errorhandler(Exception)
def default_error(error):
    return pages.error_page(error), 404

##########
# Routes
##########
@app.route('/')
def home():
    feature = content_datastore.find_content(name='About Me', one=True)
    previews = content_datastore.find_content(name='Projects', one=True)
    resume =    content_datastore.find_content(name='Resume', one=True)
    github =    content_datastore.find_content(name='Github', one=True)

    return pages.home_page([feature, previews, resume, github], feature, previews)


@app.route('/resource/<string:encrypted>')
def download_resource(encrypted):
    basename, filename = os.path.split(decrypt_resource(encrypted, request.args.get('access')))
    return send_from_directory(os.path.join(app.config.get("FILE_ROOT") or '', basename), filename)


@app.route('/<string:display_type>/<string:content>')
def content_page(display_type, content):
    content = content_datastore.find_content(name=content, display_type=display_type, one=True)
    return pages.feature_page(content)


@app.route('/login')
@auth_required()
def login():
    return "Logged In"

@app.route('/logout')
def logout():
    logout_user()
    return "Logged Out"