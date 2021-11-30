
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms.form import Form
from flask_wtf import FlaskForm
from .models import Register

class CustomerRegestrationForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', )
    email = StringField('Email: ', )
    password = PasswordField('Password: ',)
    confirm = PasswordField('Repeat password',)
    country = StringField('Country: ', )
    state = StringField('State: ', )
    city = StringField('City: ', )
    contact = StringField('Contact: ', )
    adress = StringField('Adress: ', )
    zipcode = StringField('Zip code: ',)

    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image are accepted')])

    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already in use')
    
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('This email adress is already in use')

class UncustomerRegestrationForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', )
    email = StringField('Email: ', )
    country = StringField('Country: ', )
    state = StringField('State: ', )
    city = StringField('City: ', )
    contact = StringField('Contact: ', )
    adress = StringField('Adress: ', )
    zipcode = StringField('Zip code: ',)
    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already in use')
    
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('This email adress is already in use')

class CustomerLoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    
















