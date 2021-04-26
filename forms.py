from flask_security.forms import (
            LoginForm,
            ConfirmRegisterForm,
            StringField,
            Required,
            TwoFactorSetupForm,
            unique_identity_attribute)
import bleach


class ExtendedRegisterForm(ConfirmRegisterForm):
    username = StringField('Username', validators=[Required(message='EMAIL_NOT_PROVIDED'), unique_identity_attribute])
    email = None


def username_mapper(identity):
    return bleach.clean(identity, strip=True)


class ExtendedLoginForm(LoginForm):
    # This is a hack--we're just using email to run through
    # default validation. The validation function looks up
    # users based on configured auth methods, rather than
    # field name
    email = StringField('Username', validators=[Required(message='EMAIL_NOT_PROVIDED')])
    

class ExtendedTwoFactorSetupForm(TwoFactorSetupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup.data = "authenticator"
