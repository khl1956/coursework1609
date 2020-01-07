from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField


class DashboardForm(Form):
    username = StringField("Username: ", [])

    submit = SubmitField("View user data")