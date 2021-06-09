import os
import itsdangerous

# flask and extensions
from flask import Flask, render_template, url_for, g, send_from_directory, request
from flask_security import auth_required, Security, roles_accepted, current_user
from flask_minify import minify

# internal to this app
import components
from forms import ExtendedLoginForm, username_mapper, ExtendedTwoFactorSetupForm, ExtendedRegisterForm
from models import db
from PyKxnr.config import Config, load_configuration
from cli import content, category, server
from datastore import create_user_datastore, create_content_datastore
from utils import decrypt_resource


def split_space(string):
    return string.strip().split()


app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)
app.cli.add_command(content, "content")
app.cli.add_command(category, "category")
app.cli.add_command(server, "server")

app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.filters['split_space'] = split_space

# Load configuration from file
config_file = os.environ["FLASK_CONFIG"]
load_configuration(config_file)
app.config.update(Config.common.freeze())

if app.config["ENV"] == "production":
    app.config.update(Config.production.freeze())
else:
    app.config.update(Config.development.freeze())
    # TODO: init in memory db

# Configuration options that rely on running python
app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = [{"username": {"mapper": username_mapper}}]

# initialize app and database
db.init_app(app)
security = Security(app, create_user_datastore(), login_form=ExtendedLoginForm,
                    two_factor_setup_form=ExtendedTwoFactorSetupForm,
                    confirm_register_form=ExtendedRegisterForm)

content_datastore = create_content_datastore()


@app.route('/')
def home():
    feature = content_datastore.find_content(name='About Me', one=True)
    previews = content_datastore.find_category(name='Featured Projects')
    try:
        links = [(link.ref, link.name) for link in content_datastore.find_category(name='full header').content]
    except AttributeError:
        links = []

    return components.home_page(feature=feature, previews=previews, collection=None, links=links)


@app.route('/resource/<encrypted>')
def download_resource(encrypted):
    basename, filename = os.path.split(decrypt_resource(encrypted, request.args.get('access')))
    return send_from_directory(os.path.join(app.config.get("FILE_ROOT") or '', basename), filename)


@app.route('/gallery/<string:category>/')
def category_page(category):
    category = content_datastore.find_category(name=category)
    return components.gallery_page(category)


@app.route('/c/<string:content>')
def content_page(content):
    content = content_datastore.find_content(name=content, one=True)
    # TODO: category breadcrumbs or somesuch?
    return components.article_page(content)


@app.route('/private')
@auth_required()
def private():
    return "Logged In"

if __name__ == "__main__":
    app.run()
