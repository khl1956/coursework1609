from flask_wtf import Form
from wtforms import SubmitField, FieldList, FormField, StringField, HiddenField, validators


class FieldForm(Form):
    content = StringField()
    id = HiddenField()
    nameData = HiddenField()


class GenerateTemplatesForm(Form):
    document_name = StringField('Document name', [validators.DataRequired("Enter document name"), validators.Length(min=1, message="Do not enter empty strings")])
    fields = FieldList(FormField(FieldForm), min_entries=0)

    submit = SubmitField("Generate")
