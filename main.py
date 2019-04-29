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
    # need to update templates
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
    # need to update templates
    return render_template('login.html', info=jsonify(user))

@app.route('/add_item', methods=['POST'])
def createItem():
    item = json.load(str(request.data, "utf-8"))
    email = item['email']
    if (create_item(email, item)):
        return "Success"
    # need to update templates
    return "Failure"

@app.route('/update_info', methods=['POST'])
def updateProfile():
    data = json.load(str(request.data, "utf-8"))
    info = data['info'] # which user info to update
    ret = None
    if info == "shipping":
        ret = update_shipping(data['address'], data['email'])
    elif info == "billing":
        ret = update_billing(data['address'], data['email'])
    elif info == "creditcard":
        if (data['action'] == "add"):
            ret = add_credit_card(data, data['email'])
        else: # remove
            ret = remove_credit_card(data, data['email'])
    elif info == "password":
        ret = update_password(data['password'], data['email'])
    # need to update templates
    return ret

@app.route('/add_to_cart', methods=['POST'])
def addToCart():
    data = json.load(str(request.data, "utf-8"))
    email = data['email']
    if (add_to_shopping_cart(data, email)):
        return "Success"
    # need to update templates
    return "Failure"

@app.route('/get_shopping_cart', methods=['GET'])
def getShoppingCartInfo():
    email = json.load(str(request.data, "utf-8"))['email']
    # need to update templates
    return None

@app.route('/sellers')
def list_sellers():
    return jsonify(get_sellers())

@app.route('/getTable')
def getTable():
    return jsonify(get_table(json.loads(str(request.data, "utf-8"))['table_name']))

if __name__ == '__main__':
    app.run(host='', port=8000, debug=True)
    initializedb()
