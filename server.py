"""
Class: ITAS 256
Assignment: 02 - Pizza Web Server
Name: Khaim D
Date: 04-Mar-2024


"""
from flask import Flask, request, render_template, redirect, url_for, session, abort

from LoginForm import LoginForm
from CreateForm import CreateForm
from PizzaForm import PizzaForm

from json import loads, dumps

app = Flask(__name__)
app.secret_key = 'super secret setting'

def get_file_content(filename: str) -> str:
	with open(f'{filename}') as file_:
		file_content = file_.read()
		return file_content

def new_order(type: str, crust: str, size: str, quantity: str, price_per: str, order_date) -> None:
	pizzaJSON = loads(get_file_content('data/pizzaorders.json'))

	id = max([pizza['id'] for pizza in pizzaJSON]) + 1

	new_pizza = {
		"id": id,
		"type": type,
		"crust": crust,
		"size": size,
		"quantity": int(quantity),
		"price_per": float(price_per),
		"order_date": order_date
	}

	pizzaJSON.append(new_pizza)
	with open('data/pizzaorders.json', 'w') as pizzas_file:
		pizzas_file.write(dumps(pizzaJSON, indent=2))  
	return

def edit_order(id: int, type: str, crust: str, size: str, quantity: str, price_per: str, order_date) -> None:
	pizzaJSON = loads(get_file_content('data/pizzaorders.json'))

	pizzaJSON = [pizza for pizza in pizzaJSON if pizza['id'] != id]
	pizzaJSON.append({
		"id": id,
		"type": type,
		"crust": crust,
		"size": size,
		"quantity": int(quantity),
		"price_per": float(price_per),
		"order_date": order_date
	})

	with open('data/pizzaorders.json', 'w') as pizzas_file:
		pizzas_file.write(dumps(pizzaJSON, indent=2))  
	return

def delete_order(id: int):
	pizzaJSON = loads(get_file_content('data/pizzaorders.json'))
 
	print(id)

	pizzaJSON = [pizza for pizza in pizzaJSON if pizza['id'] != id]

	with open('data/pizzaorders.json', 'w') as pizzas_file:
		pizzas_file.write(dumps(pizzaJSON, indent=2))
	return

def new_user(email: str, password: str, role: str) -> None:
	usersJSON = loads(get_file_content('data/users.json'))
 
	new_user = {
    	'email': email, 
		'password': password, 
		'role': role
    }

	usersJSON.append(new_user)
	with open('data/users.json', 'w') as users_file:
		users_file.write(dumps(usersJSON, indent=2))  
	return

def check_login(email: str, password: str) -> bool:
	user = get_user(email)

	if 'password' not in user or user['password'] != password:
		return False
	return True

def get_user(email) -> dict:
	usersJSON = loads(get_file_content('./data/users.json'))
	
	for user in usersJSON:
		if email == user['email']:
			return user
	return {}

def is_logged_in() -> bool:
	if session and 'email' in session and 'role' in session:
		return True
	return False

def compare_orders(order):
    return order['order_date']


@app.route('/')
def menu():
	if is_logged_in() == False:
		return redirect(url_for('login'))

	email = session['email']
	user = get_user(email)
 
	pizzaOrdersJSON = sorted(loads(get_file_content('./data/pizzaorders.json')), key=compare_orders, reverse=True)
 
	data = {"user": user, "orders": pizzaOrdersJSON}
 
	return render_template('index.html', data=data)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		if is_logged_in():
			return redirect(url_for('menu'))

		form = LoginForm()

		return render_template('login.html', form=form)
	elif request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		
		if check_login(email, password):
			role = get_user(email)['role']
			session['email'] = email
			session['role'] = role
			return redirect(url_for('menu'))
		else:
			return redirect(url_for('login'))
	return redirect(url_for('login'))

@app.route('/logout/')
def logout():
	if is_logged_in() == False:
		return redirect(url_for('login'))

	session.pop('email')
	session.pop('role')
	return redirect(url_for('login'))

@app.route('/create', methods=['GET', 'POST'])
def create_user():
	if request.method == 'GET':
		if is_logged_in():
				return redirect(url_for('menu'))

		form = CreateForm()

		return render_template('create.html', form=form)
	elif request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		password_confirm = request.form.get('password_confirm')
		role = request.form.get('role')
  
		if password != password_confirm:
			print(f'{password} {password_confirm}')
			print("password unconfirmed")
			return redirect(url_for('create_user'))

		if check_login(email, password):
			print("user already in system")
			return redirect(url_for('create_user'))
  
		new_user(email, password, role)

		return redirect(url_for('login'))
	return redirect(url_for('login'))

@app.route('/pizza', methods=['GET', 'POST'])
def order_pizza():
	if is_logged_in() == False:
		return redirect(url_for('login'))

	if request.method == 'GET':
		form = PizzaForm()
		return render_template('pizza.html', form=form)
	elif request.method == 'POST':
		id = request.form.get('id')
		type = request.form.get('type')

		if id != 'null' and type == None:
			delete_order(int(id))
			return redirect(url_for('menu'))
		
		crust = request.form.get('crust')
		size = request.form.get('size')
		quantity = request.form.get('quantity')
		price_per_pizza = request.form.get('price_per_pizza')
		date = request.form.get('date').replace('-', '/')
		
		if id != 'null':
			edit_order(int(id), type, crust, size, quantity, price_per_pizza, date)
			return redirect(url_for('menu'))
  
		new_order(type, crust, size, quantity, price_per_pizza, date)
		return redirect(url_for('menu'))
	return redirect(url_for('login'))

@app.route('/confirm', methods=['POST'])
def confirm():
	if is_logged_in() == False:
		return redirect(url_for('login'))

	if request.method == 'POST':
		data = loads(request.form.get('data').replace("'", '"'))
		return render_template('confirm.html', data=data)

	return redirect(url_for('menu'))

if __name__ == '__main__':
	app.run(debug=True, port=885988)