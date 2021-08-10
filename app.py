'''
As with many flask applications, this file describes the top level route layout for this website. Below this level
are pages and components, each laid out in their own file. Each of these files also corresponds to a folder of jinja
templates, in the templates folder.

From a high level, each route loads content from the database and passes it to a function from pages.py that builds
and returns a page. Within pages.py, the database content is parsed into Component objects that are composited into a
page.

Forms are a special case, as they are not built from the database. Rather, they are defined in forms.py and displayed
directly by a route. To this point, I have not needed to embed forms inline. Were I to add this, a form Content option
and frame template would allow construction of a form Component, which could then be composited into a page.

Final note, the use of Content and Category are not enforced in the application. All database queries are run before
passing the Content to the page (with the possible exception of Content that loads a preview for a Category, where the
query may be deferred until render time), so the organization of Content per page is defined by each route. Pages may,
for example, be defined as categories--though this makes ordering content challenging as there isn't currently a defined
order for the content returned from a category subquery. In any case, all queries are verified against the currently
logged in user at the level of the ORM model.
'''
import os

# flask and extensions
from flask import Flask, url_for, g, send_from_directory, request, redirect
from flask_security import auth_required, Security, roles_accepted, current_user, logout_user
from flask_minify import minify
from flask_babel import Babel

# internal to this app
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
babel = Babel(app)

##########
# Exception/Error handling
##########
@app.errorhandler(Exception)
def default_error(error):
    # TODO: log error
    return pages.error_page(error), 404

##########
# Routes
##########
@app.route('/')
def home():
    feature  = content_datastore.find_content(name='About Me', one=True)
    previews = content_datastore.find_content(name='Projects', one=True)
    resume   = content_datastore.find_content(name='Resume', one=True)
    github   = content_datastore.find_content(name='Github', one=True)

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
    return redirect('/')
