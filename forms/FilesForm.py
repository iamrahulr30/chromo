from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField
from wtforms.validators import DataRequired

class ImageFolderForm( FlaskForm ) :
    image_folder = MultipleFileField("Input Folder" , validators = [DataRequired()])
    submit = SubmitField("Submit")