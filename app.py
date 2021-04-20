import flask_login
import components
import os

from flask import Flask, render_template, url_for
from flask_security import login_required, Security, SQLAlchemyUserDatastore, hash_password
from forms import ExtendedLoginForm, username_mapper, ExtendedTwoFactorSetupForm
from models import User, Role, Content, Category, db
from sqlalchemy import event, orm, true
from functools import reduce
from PyKxnr.config import Config, load_configuration
from flask_minify import minify

app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)
app.jinja_options['extensions'].append('jinja2.ext.do')


# Load configuration from file
config_file = os.environ["FLASK_CONFIG"]
load_configuration(config_file)


# set create
app.config.update(Config.common.freeze())
if app.config["ENV"] == "production":
    app.config.update(Config.production.freeze())

    @app.before_first_request
    def create_db():
        db.create_all()
        db.session.commit()

else:
    app.config.update(Config.development.freeze())

    @app.before_first_request
    def create_user():
        db.create_all()
        if not user_datastore.find_user(username="test"):
            user_datastore.create_user(username="test", password=hash_password("password"),)
        db.session.commit()


# Configuration options that rely on running python
app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = [{"username": {"mapper": username_mapper}}]


# initialize app and database
db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=ExtendedLoginForm,
                    two_factor_setup_form=ExtendedTwoFactorSetupForm)


@event.listens_for(db.session, "do_orm_execute")
def _add_filtering_criteria(execute_state):
    '''
    Add global filter to content queries for users with
    allowed roles

    :param execute_state:
    :return:
    '''
    global request  # received from flask

    if (
            execute_state.is_select
            and not execute_state.is_column_load
            and not execute_state.is_relationship_load
    ):
        # TODO: rather than content, use a RolesRequired mixin
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                Content,
                lambda cls: reduce(lambda a, b: a & b,
                                   map(lambda a: a.in_(cls.required_roles),
                                       flask_login.current_user.roles), true()),
                include_aliases=True
            )
        )


@app.route('/')
def home():
    feature = Content.query.filter_by(id='about-me').first()
    previews = Category.query.filter_by(id='featured-projects').first()
    additional_links = {"Gallery": url_for('gallery'),
                        "Login": url_for('private')}

    return components.home_page(feature=feature, previews=previews, collection=None, additional_links=additional_links)


@app.route('/gallery/')
def gallery():
    category = Category.query.filter_by(id='project').first()
    return components.gallery_page(category)


@app.route('/private')
@login_required
def private():
    return "Logged In"


if __name__ == "__main__":
    app.run()