from flask import Flask, render_template
from flask import jsonify, request
from database import *
import json
import sqlite3

app = Flask(__name__)

@app.route('/') # home page
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST']) # register page
def register():
    if request.method == 'POST':
        acct = json.loads(str(request.data, "utf-8"))
        if (register_user(acct)):
            return "Success"
        return "Failure"
    return render_template('register.html')

@app.route('/login', methods=['GET']) # login page
def login():
    email = request.form['email']
    password = request.form['password']
    row = login_user(email, password)
    error = None
    if (row):
        firstName = row['FirstName']
        lastName = row['LastName']
        user = {
        'first': firstName,
        'last': lastName
        }
    else:
        error = True
        return render_template('login.html', error=error)
    return render_template('login.html', info = jsonify(user))

if __name__ == '__main__':
    app.run(host='', port=8000, debug=True)
    initializedb()
