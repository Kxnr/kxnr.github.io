import flask_login
import components
import os

from flask import Flask, render_template, url_for
from flask_security import auth_required, Security, SQLAlchemyUserDatastore, hash_password
from forms import ExtendedLoginForm, username_mapper, ExtendedTwoFactorSetupForm
from models import User, Role, Content, Category, db
from sqlalchemy import event, orm, true
from functools import reduce
from PyKxnr import Config, IniConfig, JsonConfig

app = Flask(__name__)

# Load configuration from file
config_file = os.env["FLASK_CONFIG"]
if os.path.getext(config_file) == "json":
    JsonConfig.load(config_file)    
elif os.path.getext(config_file) == "ini":
    IniConfig.load(config_file)
else:
    raise Exception("Unsupported configuration type")

# set create 
app.config.from_object(Config.common)
if app.config["ENV"] == "production":
    app.config.from_object(Config.production)

else:
    app.config.from_object(Config.development)

    @app.before_first_request
    def create_user():
        db.create_all()
        if not user_datastore.find_user(username="test"):
            user_datastore.create_user(username="test", password=hash_password("password"),)
        db.session.commit()


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
    additional_links = {"Gallery": url_for('gallery'), "Login": url_for('private')}
    feature = Content.query.filter_by(id='about-me').first()
    previews = Category.query.filter_by(id='featured-projects').first()
    return components.home_page(feature, previews, collection=None, additional_links=additional_links)


@app.route('/gallery/')
def gallery():
    return render_template("gallery.html")


@app.route('/private')
@auth_required()
def private():
    return "Logged In"
