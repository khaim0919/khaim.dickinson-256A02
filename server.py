"""
Class: ITAS 256
Assignment: 02 - Pizza Web Server
Name: Khaim D
Date: 04-Mar-2024


"""
from flask import Flask, request, render_template, redirect, url_for, session, abort

from json import loads, dumps

app = Flask(__name__)
app.secret_key = 'super secret setting'

def get_file_content(filename: str) -> str:
	with open(f'{filename}') as file_:
		file_content = file_.read()
		return file_content

def create_order(type: str, crust: str, size: str, quantity: str, price_per: str, order_date) -> None:
	"""
	{
		“id”: an integer a number which is the “key-value” for access the order record,
		“type”: one of the type values from the init file,
		“crust”: one of crust values from the init file, 
		“size”: one of size values from the init file,
		“quantity”: an integer,
		“price_per”: a floating point number (price per pizza),
		“order_date”: a string of the date the order was placed in the format yyyy/mm/dd
	}
	"""

	return

def create_user(email: str, password: str, role: str) -> None:
	"""
	{
		“email”: an email address,
		“password”: a password (no formatting or minimal requirements unless you want to)
		“role”: 's' for staff or 'c' for customer
	}
	"""

	return

def check_login(email: str, password: str) -> bool:
	usersJSON = loads(get_file_content('users.json'))
    
	for user in usersJSON:
		if email == user['email'] and password == user['password']:
			return True
	return False

def is_logged_in() -> bool:
	if session and session['email'] and session['role']:
		return True
	return False


@app.route('/')
def menu():
	if is_logged_in() == False:
		return redirect(url_for('login'))

	return 'Server is up and running'


@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		
		if check_login(email, password):
			session['email'] = email
			session['password'] = password
			return redirect(url_for('menu'))
		else:
			return redirect(url_for('login'))

@app.route('/logout/')
def logout():
	if is_logged_in() == False:
		return redirect(url_for('login'))

	session.pop('email')
	session.pop('role')
	return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(debug=True, port=8888)