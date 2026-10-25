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
    product = StringField('Product Name', validators=[
                          DataRequired(), Length(max=150)])
    category = SelectField('Category', choices=[(
        c, c) for c in CATEGORIES], validators=[DataRequired()])
    description = StringField('Add Description', validators=[Optional()])
    img = FileField('Upload an Image', validators=[Optional()])
    location = SelectField('Address', choices=[("", "Choose a location")] + [
                           (loc, loc) for loc in LOCATIONS], validators=[DataRequired()])
    store = SelectField('Store', choices=[(
        "", "Choose a store"), ("__new__", "Add a new store...")], validators=[DataRequired()])
    store_name = StringField("New Store Name", validators=[
                             Optional(), Length(max=150)])
    quantity = IntegerField('Product Quantity', default=1, validators=[
                            DataRequired(), NumberRange(min=1)])
    total_price = DecimalField('Total Price (₱)', places=2, validators=[
                               DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')


class CompareForm(FlaskForm):
    product1 = StringField('First Product', validators=[DataRequired()])
    product2 = StringField('Second Product', validators=[DataRequired()])
    submit = SubmitField('Compare')
