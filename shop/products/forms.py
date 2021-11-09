

from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField




class Addproducts(Form):
    name = StringField('Name', [validators.data_required()])
    price = DecimalField('Price', [validators.data_required()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.data_required()])
    description = TextAreaField('Description', [validators.data_required()])
    colors = TextAreaField('Colors', [validators.data_required()])
    img_1 = TextAreaField('Images', validators=[FileRequired()])
    img_2 = TextAreaField('Images', validators=[FileRequired()])
    img_3 = TextAreaField('Images', validators=[FileRequired()])
    












