from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField
from wtforms import validators


class UsersForm(Form):
    username = StringField("Username: ", [
        validators.DataRequired("Enter username."),
        validators.Length(min=6, message="Username should be more than 5 symbols")
    ])

    password = PasswordField("Password: ", [
        validators.DataRequired("Enter a password.")
    ])

    email = StringField("E-mail: ", [
        validators.DataRequired("Enter e-mail"),
        validators.Email("Enter valid e-mail")
    ])

    submit = SubmitField("Save")