from flask import Flask, render_template
from flask import jsonify, request
from database import *
from cart import *
from item import *
from review import *
import json
import sqlite3

app = Flask(__name__)

@app.route('/') # home page
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST']) # register page
def register():
    error = None
    if request.method == 'POST':
        acct = json.loads(str(request.data, "utf-8"))
        ret = register_user(acct)
        if (not ret):
            error = "User with that email already registered"
    return jsonify(success=ret,error=error)

@app.route('/login', methods=['GET']) # login page
def login():
    data = json.loads(str(request.data, "utf-8"))
    email = data['email']
    password = data['password']
    row = login_user(email, password)
    success = True
    error = None
    if (row == {}):
        error = "Please enter a valid email address or password"
        success = False
    return jsonify(user=row, error=error, success=success)

@app.route('/add_item', methods=['POST'])
def createItem():
    item = json.loads(str(request.data, "utf-8"))
    email = item['email']
    ret = create_item(email, item)
    return jsonify(success=ret)

@app.route('/update_info', methods=['POST'])
def updateProfile():
    data = json.loads(str(request.data, "utf-8"))
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
    return jsonify(success=ret)

@app.route('/add_to_cart', methods=['POST'])
def addToCart():
    data = json.loads(str(request.data, "utf-8"))
    email = data['email']
    ret = add_to_shopping_cart(data, email)
    return jsonify(success=ret)

@app.route('/get_shopping_cart', methods=['GET'])
def getShoppingCartInfo():
    email = json.loads(str(request.data, "utf-8"))['email']
    # need to update templates
    return jsonify(get_shopping_cart_data(email))

@app.route('/delete_from_cart', methods=['POST'])
def removeFromCart():
    data = json.loads(str(request.data, "utf-8"))
    email = data['email']
    ret = delete_from_shopping_cart(data, email)
    return jsonify(success=ret)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = json.loads(str(request.data, "utf-8"))
    email = data['email']
    ret = checkout_cart(email, data)
    return jsonify(success=ret, error="Bad POST request or cart is empty")

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify(get_users())

@app.route('/items', methods=['GET'])
def list_items():
    return jsonify(get_all_items())

@app.route('/item_by_user', methods=['GET'])
def list_items_by_user():
    return jsonify(get_all_items_user(json.loads(str(request.data, "utf-8"))['email']))

@app.route('/delete_item_from_user', methods=['POST'])
def delete_item_from_user():
    r = json.loads(str(request.data, "utf-8"))
    ret = delete_item_user(r['email'], r['id'])
    return jsonify(success=ret)

@app.route('/purchases_for_user', methods=['GET'])
def get_purchases_for_user():
    return jsonify(get_purchases(json.loads(str(request.data, "utf-8"))['email']))

@app.route('/getTable')
def getTable():
    return jsonify(get_table(json.loads(str(request.data, "utf-8"))['table_name']))

if __name__ == '__main__':
    app.run(host='', port=8000, debug=True)
    initializedb()
