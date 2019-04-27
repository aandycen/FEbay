from flask import Flask, render_template
from flask import jsonify, request
from database import *
import sqlite3

app = Flask(__name__)

@app.route('/') # home page
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST']) # register page
def register():
    first = request.form['firstname']
    last = request.form['lastname']
    password = request.form['password']
    email = request.form['email']
    acct = {'first':first,'last':last, 'email':email, 'password':password}
    register_user(acct)
    return render_template('register.html')

@app.route('/login', methods=['GET']) # login page
def login():
    email = request.form['email']
    password = request.form['password']
    row = login_user(email, password)
    if (row):
        firstName = row['FirstName']
        lastName = row['LastName']
        user = {
        'first': firstname,
        'last': lastName
        }
    return render_template('login.html', info = jsonify(user))

if '__name__' == '__main__':
    app.run()
    initializedb()
