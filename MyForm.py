from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, FileField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import ValidationError
from PIL import Image


def validate_image(self, image):
    if image.data:
        img = Image.open(image.data)
        width, height = img.size
        aspect_ratio = [width / height != 2 / 3]
        if not 0.63 < aspect_ratio < 0.7:
            raise ValidationError('Image aspect ratio must be 2:3')
        if width < 250 or height < 380:
            raise ValidationError('Image resolution low')

class MovieForm(FlaskForm):
    name = StringField('Titel', validators=[DataRequired()])
    description = TextAreaField('Description')
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1990, max=2030)])
    rating = FloatField('Rating', validators=[NumberRange(min=0, max=10)])
    banner = FileField('Upload Banners')

class DeleteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Delete')

class EditForm(FlaskForm):
    movie_id = IntegerField('id', validators=[DataRequired()])
    name = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1990, max=2030)])
    rating = FloatField('Rating', validators=[NumberRange(min=0, max=10)])
    banner = FileField('Upload Banners')
