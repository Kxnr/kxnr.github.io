from flask import Flask, render_template
from flask_security import auth_required, Security, SQLAlchemyUserDatastore, hash_password
from forms import ExtendedLoginForm, username_mapper, ExtendedTwoFactorSetupForm
from models import User, Role, RoleUser, db

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

@app.before_first_request
def create_user():
    db.create_all()
    if not user_datastore.find_user(username="test"):
        user_datastore.create_user(username="test", password=hash_password("password"),)
                                   # tf_totp_secret=, tf_primary_method="authenticator")
    db.session.commit()

@app.route('/')
def home():
    return render_template("pages/home.html")

@app.route('/gallery/')
def gallery():
    return render_template("gallery.html")

@app.route('/private')
@auth_required()
def private():
    return "Logged In"