from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class FieldsForm(Form):
    template_id = IntegerField("Template ID: ", [
        validators.DataRequired("Enter template ID"),
        validators.NumberRange(min=1, message="Min ID value is 1")
    ])

    field_name = StringField("Name: ", [
        validators.DataRequired("Enter field name"),
        validators.Length(min=1, message="Do not enter empty strings")
    ])

    field_content = StringField("Content: ", [])

    submit = SubmitField("Save")