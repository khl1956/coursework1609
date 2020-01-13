from flask_wtf import Form
from wtforms import *


class DocumentsForm(Form):
    document_name = StringField("Document name: ", [
        validators.DataRequired("Enter document name"),
        validators.Length(min=1, message="Do not enter empty strings")
    ])

    file = FileField("Document file")

    submit = SubmitField("Save")