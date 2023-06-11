from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, FloatField, SubmitField, IntegerField, FieldList, validators

class MyForm(FlaskForm):
    title = StringField('Title', validators=[validators.DataRequired(), validators.Length(min=1)])
    description = StringField('Description', validators=[validators.DataRequired(), validators.Length(min=10)])
    imdb_rating = FloatField('Imdb Rating', validators=[validators.DataRequired()])
    year = IntegerField('Year', validators=[validators.DataRequired()])
    genres = FieldList(StringField('Genres', validators=[validators.DataRequired()]))
    directors = FieldList(StringField('Directors', validators=[validators.DataRequired()]))
    image = FileField('image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')