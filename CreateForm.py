from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField, PasswordField, SelectField
from wtforms import validators, ValidationError

class CreateForm(Form):
    email = StringField("Email",[validators.Email("Please enter a valid email address.")])
    password = PasswordField("Password",[validators.InputRequired("A password is required")])
    password_confirm = PasswordField("Verify Password",[validators.InputRequired("You must confirm your password")])
    role = RadioField("Role", choices=[('s', 'Staff'), ('c', 'Customer')])
    submit = SubmitField('Create')