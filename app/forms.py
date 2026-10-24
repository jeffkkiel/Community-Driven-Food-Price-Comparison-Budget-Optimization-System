from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired



class ProductForm(FlaskForm):
    product = StringField('Product Name', validators=[DataRequired()])

    submit = SubmitField('Add Product')

class CompareForm(FlaskForm):
    product1 = StringField('First Product', validators=[DataRequired()])
    product2 = StringField('Second Product', validators=[DataRequired()])
    submit = SubmitField('Compare')
