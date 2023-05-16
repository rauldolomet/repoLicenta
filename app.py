
from flask import Flask, jsonify, redirect, request, render_template, url_for
import requests
import json
from fastapi import FastAPI
from datetime import datetime
import boto3
import key_config as keys

app = Flask(__name__)


dynamoDB = boto3.resource('dynamodb')


table = dynamoDB.create_table(
    TableName='udkjfdfst324241',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'password',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'password',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        
    }
)


print("Items in the AWS table: " + str(table.item_count))

'''
Define some basic level users.
These users will only benefit from a restricted
access level.
'''

users = {
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
    err = None
    if request.method == 'POST':
        if request.form.get('username') in users.keys() or request.form.get('username')=="":
            return redirect(url_for('displaySelectedUser'))
    err = "Couldn't find user"
    return render_template('scanUsers.html', err=err)


'''
The other option available for the moment is
creating a new entry in the system. This route 
allows the user to register a new dataset into the system which 
willa utomatically be loaded into the AWS Database
'''


@app.route('/create', methods=['GET', 'POST'])
def createUsers():
    if request.method == 'POST':
        pass
    return render_template('createUser.html')


@app.route('/results', methods=['GET', 'POST'])
def displaySelectedUser():
    if request.method == 'POST':
        return redirect(url_for('getAWSData'))

    return render_template('selectedUser.html')


@app.route('/NotFoundErr')
def userNotFoundErr():
    return "err user not found"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
