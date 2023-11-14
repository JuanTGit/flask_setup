from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ProductUpdate(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    category = SelectField('Category')
    submit = SubmitField('Update Product')
    create = SubmitField('Create Product')