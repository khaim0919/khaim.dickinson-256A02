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

def get_file(filename: str) -> str:
    with open(f'{filename}') as file_:
        file_content = file_.read()
        return file_content


@app.route('/')
def default():
    return 'Server is up and running'



if __name__ == '__main__':
    app.run(debug=True, port=9008)