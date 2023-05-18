
from flask import Flask, jsonify, redirect, request, render_template, url_for
import requests
import json
from fastapi import FastAPI
from datetime import datetime
import boto3
import key_config as keys
import time
app = Flask(__name__)


'''
Define some basic level users.
These users will only benefit from a restricted
access level.
'''

users = {
    'ted' : 'bundy',
    'raul': 'Raul1611@',
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
The login route will check for 
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
            error = "Invalid credentials -> Username or password not found ! "
    return render_template('login.html', error=error)


'''
The home route leads to the "homepage" of
the project. This is where the user decides whether 
they want to create a new entry in the system
or scan for an already existing user
'''


@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST' and request.form.get('action') == 'scan':
        return redirect(url_for('scanUsers'))
    if request.method == 'POST' and request.form.get('action') == 'create':
        return redirect(url_for('createUsers'))
    return render_template('homepage.html')


'''
The first choice of the two presented in the homepage
is te scanning one. This will search througth the 
linked database filtering based on the keywords 
the users enter and either return an err message
or a(some) record(s) found
'''


@app.route('/scan', methods=['GET', 'POST'])
def scanUsers():
    if request.method == 'POST':
        if request.form.get('username') in users.keys():
            return redirect(url_for('displaySelectedUser'))
        else:
            if request.form.get('username') == "" or request.form.get('username') is None: 
                err = None
            else:
                err = " User not found"

    return render_template('scanUsers.html', err=err)


'''
The other option available for the moment is
creating a new entry in the system. This route 
allows the user to register a new dataset into the system which 
willa utomatically be loaded into the AWS Database
'''


@app.route('/create', methods=['GET', 'POST'])
def createUsers():
    msg = None
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    crime = request.form.get('crime')
    represents_immediate_danger = request.form.get('represents_immediate_danger')
    if request.method == 'POST':
        client = boto3.resource('dynamodb')
        table = client.Table('Convicted_Fellons')
        input={
                'first_name': first_name if first_name is not None else "*",
                'last_name': last_name if last_name is not None else "*",
                'crime': crime if crime is not None else "*",
                'represents_immediate_danger': represents_immediate_danger if represents_immediate_danger is not None else "*"}
        table.put_item(Item=input)
        table.delete_item(Key={'first_name':'*'})
    if first_name is not None and last_name is not None: 
        msg = "Successfully added " + str(first_name) + " " + str(last_name)
        time.sleep(2)
        return redirect(url_for('createUsers'))
    return render_template('createUser.html', msg=msg)

@app.route('/results', methods=['GET', 'POST'])
def displaySelectedUser():
        response = None
        client = boto3.resource('dynamodb')
        table = client.Table('Convicted_Fellons')
        scanned = request.form.get('username')
        response = table.get_item(Key={'first_name': 'ted' })
        response = response['Item']
        response_fname = {'First name ': response['first_name']}
        response_lname = {'Last name: ': response['last_name']}
        response_crime = {'Crime commited ': response['crime']}
        response_danger = {'Represents an immediate danger': response['represents_immediate_danger']}
        return render_template('selectedUser.html', response_fname = response_fname, response_lname = response_lname, response_crime = response_crime, response_danger = response_danger)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
