from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class TemplatesForm(Form):
    user_id = IntegerField("User ID: ", [
        validators.DataRequired("Enter user ID"),
        validators.NumberRange(min=1, message="Min ID value is 1")
    ])

    template_name = StringField("Template name: ", [
        validators.DataRequired("Enter template name"),
        validators.Length(min=1, message="Do not enter empty strings")
    ])

    submit = SubmitField("Save")