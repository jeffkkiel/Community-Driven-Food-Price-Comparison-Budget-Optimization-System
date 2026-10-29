from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Optional, NumberRange, Length, ValidationError, EqualTo

CATEGORIES = [
    "Fruits", "Vegetables", "Meat", "Seafood", "Chilled", "Frozen", "Snacks", "Sweets", "Beverages"
]

LOCATIONS = [
    "Bacoor, Cavite", "Dasmariñas, Cavite", "Imus, Cavite", "Lopez, Quezon", "New York City, New York",
    "Cavite City, Cavite", "General Trias, Cavite", "Tagaytay, Cavite", "Trece Martires, Cavite", "Kawit, Cavite", "Silang, Cavite",
    "Manila, Metro Manila", "Quezon City, Metro Manila", "Makati, Metro Manila", "Pasig, Metro Manila", "Taguig, Metro Manila",
    "Cebu City, Cebu", "Davao City, Davao del Sur", "Baguio, Benguet", "Iloilo City, Iloilo", "Cagayan de Oro, Misamis Oriental",
    "Los Angeles, California", "Chicago, Illinois", "Tokyo, Japan", "Singapore, Singapore", "London, United Kingdom",
    "Sydney, Australia", "Dubai, United Arab Emirates", "Hong Kong, Hong Kong",
]


class AuthForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[Optional()])
    submit = SubmitField('Continue')

class ProductForm(FlaskForm):
    category = SelectField('Category', choices=[(c, c) for c in CATEGORIES], validators=[DataRequired()])
    product = SelectField('Product Name', choices=[], validators=[DataRequired()])
    product_name = StringField("New Product Name", validators=[Optional(), Length(max=150)])
    description = StringField('Add Description', validators=[Optional()])
    img = FileField('Upload an Image', validators=[Optional()])
    location = SelectField('City', choices=[("", "Choose a city")] + [(loc, loc) for loc in LOCATIONS], validators=[DataRequired()])
    store = SelectField('Store', choices=[], validators=[DataRequired()])
    store_name = StringField("New Store Name", validators=[Optional(), Length(max=150)])
    quantity = IntegerField('Product Quantity', default=1, validators=[DataRequired(), NumberRange(min=1)])
    total_price = DecimalField('Total Price (₱)', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')


class CompareForm(FlaskForm):
    products = SelectMultipleField('Add a food to compare',choices=[], validators=[DataRequired()])
    submit = SubmitField('Add')
