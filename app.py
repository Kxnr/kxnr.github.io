
import flask_login
import components
import os

from flask import Flask, render_template, url_for, g
from flask_security import auth_required, Security, roles_accepted
from forms import ExtendedLoginForm, username_mapper, ExtendedTwoFactorSetupForm, ExtendedRegisterForm
from models import db
from PyKxnr.config import Config, load_configuration
from flask_minify import minify
from cli import content, category
from datastore import create_user_datastore, create_content_datastore


def split_space(string):
    return string.strip().split()


app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)
app.cli.add_command(content, "content")
app.cli.add_command(category, "category")
app.jinja_options['extensions'].append('jinja2.ext.do')
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



# initialize app and database
db.init_app(app)
security = Security(app, create_user_datastore(), login_form=ExtendedLoginForm,
                    two_factor_setup_form=ExtendedTwoFactorSetupForm,
                    confirm_register_form=ExtendedRegisterForm)

content_datastore = create_content_datastore()


@app.route('/')
def home():
    feature = content_datastore.find_content(name='About Me', user=flask_login.current_user, one=True)
    previews = content_datastore.find_content(categories='Featured Projects')
    additional_links = {"Gallery": url_for('gallery'),
                        "Login": url_for('private')}

    return components.home_page(feature=feature, previews=previews, collection=None, additional_links=additional_links)


@app.route('/gallery/')
def gallery():
    # category = Category.query.filter_by(name='project').first()
    category = content_datastore.find_content(categories='project')
    return components.gallery_page(category)


@app.route('/private')
@auth_required()
def private():
    return "Logged In"


if __name__ == "__main__":
    app.run()
