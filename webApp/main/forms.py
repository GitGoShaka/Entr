from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')


class PDFUploadForm(FlaskForm):
    pdf_file = FileField('Upload PDF', validators=[DataRequired(), FileAllowed(['pdf'])])
    submit = SubmitField('Process PDF')