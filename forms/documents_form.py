from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class DocumentsForm(Form):
    user_id = IntegerField("User ID: ", [
        validators.DataRequired("Enter user ID"),
        validators.NumberRange(min=1, message="Min ID value is 1")
    ])

    document_name = StringField("Document name: ", [
        validators.DataRequired("Enter document name"),
        validators.Length(min=1, message="Do not enter empty strings")
    ])

    submit = SubmitField("Save")