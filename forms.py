from flask_security.forms import (
            LoginForm,
            StringField,
            Required,
            RegisterForm,
            StringField,
            Required,
            TwoFactorSetupForm)
import bleach

class ExtendedRegisterForm(RegisterForm):
    email = StringField('Username', validators=[Required(message='EMAIL_NOT_PROVIDED')])

def username_mapper(identity):
    return bleach.clean(identity, strip=True)

class ExtendedLoginForm(LoginForm):
    email = StringField('Username', validators=[Required(message='EMAIL_NOT_PROVIDED')])

class ExtendedTwoFactorSetupForm(TwoFactorSetupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup.data = "authenticator"
