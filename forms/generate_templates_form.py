from flask_wtf import Form
from wtforms import SubmitField, FieldList, FormField, StringField


class FieldForm(Form):
    content = StringField()

class GenerateTemplatesForm(Form):
    fields = FieldList(FormField(FieldForm), min_entries=0)

    submit = SubmitField("Generate")
