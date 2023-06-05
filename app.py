
from flask import Flask, jsonify, redirect, request, render_template, url_for, session
import requests
import json
from fastapi import FastAPI
from datetime import datetime
import boto3
import key_config as keys
import time
from boto3.dynamodb.conditions import Key
import bcrypt
import os
import geocoder
import folium
import smtplib

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'

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
        username = request.form.get('username')
        password = request.form.get('password')
        salt = bcrypt.gensalt()
        pass_hash = bcrypt.hashpw(str(password).encode('utf-8'), salt)
        client = boto3.resource('dynamodb')
        table = client.Table('usersTable')
        user_exists = table.query(
            KeyConditionExpression=Key('username').eq(str(username)))
        if len(user_exists['Items']) > 0:
            for user in user_exists['Items']:
                if bcrypt.checkpw(str(password).encode('utf-8'),
                                  user['pass_hash'].encode('utf-8')):
                    return redirect(url_for('homepage'))
                else:
                    error = "Invalid credentials. Username or password not found ! "
                    return render_template('login.html', error=error)
        else:
            error = "Invalid credentials. Username or password not found ! "
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
    danger_color_code = None
    if request.method == 'GET':
        scanned_user = request.args.get('uuid')
        client = boto3.resource('dynamodb')
        table = client.Table('Convicted_Fellons')
        response = table.query(
            KeyConditionExpression=Key('uuid').eq(scanned_user))
        if len(response['Items']) > 0:
            full_response = response
            uuid = response['Items'][0]['uuid']
            first_name = response['Items'][0]['first_name']
            last_name = response['Items'][0]['last_name']
            crime = response['Items'][0]['crime']
            dangerous = response['Items'][0]['represents_immediate_danger']
            danger_color_code = 'red' if dangerous.lower() != 'no' else '#26f107'
            print("User scanned : " + str(scanned_user))
            print("Response aws: " + str(response['Items']))
            print("Danger code: " + danger_color_code)
            return render_template(
                'selectedUser.html',
                full_response=full_response,
                uuid=uuid,
                first_name=first_name,
                last_name=last_name,
                crime=crime,
                dangerous=dangerous,
                danger_color_code=danger_color_code)
        else:
            err = f"Couldn't find records for '{scanned_user}'"
            return render_template('scanUsers.html', err=err)
    return render_template('scanUsers.html', err=err)


@app.route('/alert', methods=['GET', 'POST'])
def alertFellonPresence():
    message = None
    if request.method == 'POST':
        location = str(geocoder.ip("me").latlng)
        latitude = geocoder.ip("me").latlng[0]
        longitude = geocoder.ip("me").latlng[1]
        email_message = f'Criminal activity spotted at these coordinates: \n Latitude: {latitude} \n Longitude: {longitude}\n Please take immediate action!'
        email_subject = 'Hostile presence reported'
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('rauldolomet@gmail.com', 'bwuuwpqftbrinhsw')
            msg = f'''
            Subject: {email_subject}\n\n\n {email_message} \n\n 
This automated email serves as an urgent alert to inform you about a reported hostile presence in the area. Immediate action is advised to ensure public safety and prevent any potential harm.


Please dispatch the appropriate authorities to the location mentioned above to assess the situation, neutralize any threats, and ensure the safety of the community. Swift response and deployment of necessary resources are vital in resolving this situation effectively.

For any additional information or assistance required, please feel free to contact me directly at [Your Contact Information]. I am ready to cooperate fully with law enforcement officials to facilitate a swift resolution.

Thank you for your immediate attention and cooperation in addressing this matter promptly.
            '''
            smtp.sendmail('rauldolomet@gmail.com', 'rauldolomet@gmail.com', msg)
            
        message = "Alerted authorities via e-mail"
        print("Location: " + str(location))
    return render_template('alertAuthorities.html',
                           latitude=latitude, longitude=longitude, message=message)


'''
The other option available for the moment is
creating a new entry in the system. This route
allows the user to register a new dataset into the system which
will automatically be loaded into the AWS Database
'''


@app.route('/create', methods=['GET', 'POST'])
def createUsers():
    msg = None
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    uuid = request.form.get('uuid')
    crime = request.form.get('crime')
    represents_immediate_danger = request.form.get(
        'represents_immediate_danger')
    if request.method == 'POST':
        client = boto3.resource('dynamodb')
        table = client.Table('Convicted_Fellons')
        input = {
            'uuid': uuid if uuid is not None else "*",
            'first_name': first_name if first_name is not None else "*",
            'last_name': last_name if last_name is not None else "*",
            'crime': crime if crime is not None else "*",
            'represents_immediate_danger': represents_immediate_danger if represents_immediate_danger is not None else "*"}
        table.put_item(Item=input)
        table.delete_item(Key={'uuid': '*'})
        return redirect(url_for('createUsers'))
    return render_template('createUser.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
