from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Optional, NumberRange



class ProductForm(FlaskForm):
    product = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Add Description', validators=[Optional()])
    img = FileField('Upload an Image')
    store = StringField('Which Store?', coerce=int, validators=[DataRequired()])
    #temp maganda kung may drop down tas pwede magsearch ng existing store, o magadd ng bago
    price = DecimalField('Price', places = 2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')

class CompareForm(FlaskForm):
    product1 = StringField('First Product', validators=[DataRequired()])
    product2 = StringField('Second Product', validators=[DataRequired()])
    submit = SubmitField('Compare')
