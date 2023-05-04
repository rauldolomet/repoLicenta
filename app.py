
from flask import Flask, jsonify, redirect, request, render_template, url_for
import requests
import json
from fastapi import FastAPI
from datetime import datetime


app = Flask(__name__)

'''
Define some basic level users.
These users will only benefit from a restricted
access level.
''' 

users = {
    'raul': 'raul',
    'alex': 'alex',
    'steph': 'steph',
    'admin': 'admin'
}

'''
Define some special "priviledged" users.
These users will have increased access level.
'''

priviledged_users = {
    'admin': 'admin'
}


'''
Create a default route.
This will redirect to the login page.
Without a default route, one would
first hit the 404 Not Found page,
having to manually navigate to the 
login route
'''

@app.route('/')
def default():
    return redirect(url_for('login'))

'''
The login route lwill check for 
the users input to establish the level of access they
are granted and returns a details page with either partially
clasiified information or fully disclosed data depending on
the user's permissions
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') in users.keys() and request.form.get('password') == users.get(request.form.get('username')):
            user_details = {
                'user': request.form.get('username'),
                'password': len(str(request.form.get('password'))) * '*' if request.form.get('username') != 'admin' else request.form.get('password'),
                'logged_in_at': datetime.now(),
                'user_type': 'basic' if request.form.get('username') not in priviledged_users else 'pirviledged'
            }
            return redirect(url_for('homepage'))
        else:
            error = "Invalid credentials - username or password not found ! "
    return render_template('login.html', error=error)


@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST' and request.form.get('action') == 'scan':
        return redirect(url_for('scanUsers'))
    if request.method == 'POST' and request.form.get('action') == 'create':
        return redirect(url_for('createUsers'))
    return render_template('homepage.html')


@app.route('/scan', methods=['GET','POST'])
def scanUsers():
    if request.method == 'POST':
        pass
    return render_template('scanUsers.html')

@app.route('/create', methods=['GET','POST'])
def createUsers():
    if request.method == 'POST':
        pass
    return render_template('createUser.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
