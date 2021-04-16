from flask import Flask, render_template, url_for
from flask_security import auth_required, Security, SQLAlchemyUserDatastore, hash_password
from forms import ExtendedLoginForm, username_mapper, ExtendedTwoFactorSetupForm
from models import User, Role, Content, Category, db
from sqlalchemy import event, orm, true
from functools import reduce
import flask_login
import components

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECURITY_PASSWORD_SALT"] = "test1234"
app.config["SECRET_KEY"] = "test1234"
app.config["SECURITY_CONFIRMABLE"] = False
app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = [{'username': {'mapper': username_mapper}}, ]
app.config["SECURITY_PASSWORD_HASH"] = "bcrypt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECURITY_MSG_INVALID_PASSWORD"] = ("Bad username or password", "error")
app.config["SECURITY_MSG_PASSWORD_NOT_PROVIDED"] = ("Bad username or password", "error")
app.config["SECURITY_MSG_USER_DOES_NOT_EXIST"] = ("Bad username or password", "error")
app.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['authenticator', ]
app.config['SECURITY_TWO_FACTOR'] = True
app.config['SECURITY_TWO_FACTOR_REQUIRED'] = True
app.config['SECURITY_TWO_FACTOR_ALWAYS_VALIDATE'] = True

# Generate a good totp secret using: passlib.totp.generate_secret()
app.config['SECURITY_TOTP_SECRETS'] = {"1": "TjQ9Qa31VOrfEzuPy4VHQWPCTmRzCnFzMKLxXYiZu9B"}
app.config['SECURITY_TOTP_ISSUER'] = "kxnr"

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
        print(execute_state.statement)
        # TODO: rather than content, use a RolesRequired mixin
        # TODO: what if no relationship is set for Roles?
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                Content,
                lambda cls: reduce(lambda a, b: a & b,
                                   map(lambda a: a.in_(cls.required_roles),
                                       flask_login.current_user.roles), true()),
                include_aliases=True
            )
        )


@app.before_first_request
def create_user():
    db.create_all()
    if not user_datastore.find_user(username="test"):
        user_datastore.create_user(username="test", password=hash_password("password"),)
    db.session.commit()


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