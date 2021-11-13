

from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('First Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address',[validators.Length(min=6, max=25)])#, validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('Comfirm Password', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])