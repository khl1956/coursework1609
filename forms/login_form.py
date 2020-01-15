from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms import validators


class LoginForm(Form):
    username = StringField("Username: ", [
        validators.DataRequired("Enter username."),
        validators.Length(min=6, message="Username should be more than 5 symbols")
    ])

    password = PasswordField("Password: ", [
        validators.DataRequired("Enter a password.")
    ])

    submit = SubmitField("Login")
