from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField, PasswordField
from wtforms import validators, ValidationError

class LoginForm(Form):
    email = StringField("Email",[validators.Email("Please enter a valid email address.")])
    password = PasswordField("Password",[validators.InputRequired("Password is a required field")])
    submit = SubmitField('Login')