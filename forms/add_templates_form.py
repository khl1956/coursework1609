from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, validators, SubmitField


class AddTemplatesForm(Form):
    template_name = StringField("Template name: ", [
        validators.DataRequired("Enter template name"),
        validators.Length(min=1, message="Do not enter empty strings")
    ])

    file = FileField("Template file", [
    ])

    submit = SubmitField("Save")
