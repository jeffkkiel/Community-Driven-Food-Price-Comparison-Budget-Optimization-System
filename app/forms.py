from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Optional, NumberRange, Length, ValidationError

CATEGORIES = [
    "Fruits", "Vegetables", "Meat", "Seafood", "Chilled", "Frozen", "Snacks", "Sweets", "Beverages"
]

LOCATIONS = [
    "Bacoor, Cavite", "Dasmariñas, Cavite", "Imus, Cavite", "Lopez, Quezon", "New York City, New York"
]


class ProductForm(FlaskForm):
    product = SelectField('Product Name', choices=[], validators=[DataRequired()])
    product_name = StringField("New Product Name", validators=[
                             Optional(), Length(max=150)])
    category = SelectField('Category', choices=[(
        c, c) for c in CATEGORIES], validators=[DataRequired()])
    description = StringField('Add Description', validators=[Optional()])
    img = FileField('Upload an Image', validators=[Optional()])
    location = SelectField('Address', choices=[("", "Choose a location")] + [
                           (loc, loc) for loc in LOCATIONS], validators=[DataRequired()])
    store = SelectField('Store', choices=[], validators=[DataRequired()])
    store_name = StringField("New Store Name", validators=[
                             Optional(), Length(max=150)])
    quantity = IntegerField('Product Quantity', default=1, validators=[
                            DataRequired(), NumberRange(min=1)])
    total_price = DecimalField('Total Price (₱)', places=2, validators=[
                               DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')


class CompareForm(FlaskForm):
    product = SelectField('Add a food to compare', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add')
