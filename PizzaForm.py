from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField, SelectField, FloatField
from wtforms import validators, ValidationError

from json import loads, dumps

class PizzaForm(Form):
    with open('./data/init.json') as file_:
        init = loads(file_.read())

    type = SelectField("Type", choices=init['type'])
    crust = SelectField("Crust", choices=init['crust'])
    size = SelectField("Size", choices=init['size'])
    
    quantity = IntegerField("Quantity",[validators.NumberRange(min=1, max=10)])
    price_per_pizza = FloatField("Price Per Pizza")
    
    date = DateField("Date")
    
    submit = SubmitField('Create')