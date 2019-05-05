from flask import Flask, render_template
from flask import jsonify, request
from database import *
from cart import *
from item import *
from review import *
from card import *
from purchase import *
import json
import sqlite3

app = Flask(__name__)

@app.route('/') # home page
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST']) # register page
def register():
    if request.method == 'POST':
        try:
            error = None
            acct = json.loads(str(request.data, "utf-8"))
            password = str(acct['password'])
            if (len(password) < 8):
                return jsonify(success=False, error="Password must be at least eight characters")
            if (acct['email'].count('@') != 1):
                return jsonify(success=False, error="Please enter a valid email address")
            if (len(acct['first']) == 0 or len(acct['last']) == 0):
                return jsonify(success=False, error="One or more fields are empty")
            ret = register_user(acct)
            if (not ret):
                error = "User with that email already exists"
            return jsonify(success=ret, error=error)
        except:
            return jsonify(success=False, error="Bad POST Request")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST']) # login page
def login():
    if request.method == 'POST':
        try:
            data = json.loads(str(request.data, "utf-8"))
            email = data['email']
            password = data['password']
            success = True
            error = None
            if (login_user(email, password) == {}):
                error = "Please enter a valid email address or password"
                success = False
            return jsonify(success=success, error=error)
        except:
            return jsonify(success=False, error="Bad POST Request")
    return render_template('login.html')

@app.route('/account', methods=['GET', 'POST'])
def get_user_info():
    if request.method == 'POST':
        email = json.loads(str(request.data, "utf-8"))['email']
        return jsonify(get_user(email))
    return render_template('account.html')

@app.route('/purchase_history')
def render_purchase():
    return render_template('purchasehistory.html')

@app.route('/post_item')
def render_item():
    return render_template('postitem.html')

@app.route('/checkout')
def render_checkout():
    return render_template('checkout.html')

@app.route('/cart')
def render_cart():
    return render_template('cart.html')

@app.route('/add_item', methods=['POST'])
def add_item():
    data = json.loads(str(request.data, "utf-8"))
    email = data['email']
    try:
        item = {'price':data['price'],'quantity':data['quantity'],'name':data['name'],'link':data['link']}
        create_item(email, item)
    except:
        return jsonify(success=False, error="There was a problem adding the item")
    return jsonify(success=True, message="Item added successfully")

@app.route('/update_info', methods=['POST'])
def update_profile():
    data = json.loads(str(request.data, "utf-8"))
    info = data['info'] # which user info to update
    ret = None
    message = ""
    if info == "shipping":
        ret = update_shipping(data['address'], data['email'])
        if (ret):
            message = "Shipping address updated successfully"
        else:
            message = "There was a problem updating your shipping address"
    elif info == "billing":
        ret = update_billing(data['address'], data['email'])
        if (ret):
            message = "Billing address updated successfully"
        else:
            message = "There was a problem updating your billing address"
    elif info == "creditcard":
        action = data['action']
        if (action == "add"):
            ret = add_credit_card(data, data['email'])
            if (ret):
                message = "Credit card added successfully"
            else:
                message = "There was a problem adding your credit card"
        elif (action == "remove"):
            ret = remove_credit_card(data, data['email'])
            if (ret):
                message = "Credit card removed successfully"
            else:
                message = "There was a problem removing your credit card"
        elif (action == "update"):
            ret = update_credit_card(data, data['email'])
            if (ret):
                message = "Credit card updated successfully"
            else:
                message = "There was a problem updating your credit card"
        else:
            return jsonify(succes=False, error="Bad POST Request")
    elif info == "password":
        ret = update_password(data['password'], data['email'])
        if (ret):
            message = "Password updated successfully"
        else:
            message = "There was problem updating your password"
    return jsonify(success=ret, message=message)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    ret = True
    try:
        data = json.loads(str(request.data, "utf-8"))
        email = data['email']
        item = {'id':data['id'],'quantity':data['quantity']}
        ret = add_to_shopping_cart(item, email)
    except:
        return jsonify(success=False, error="Bad POST Request")
    if (not ret):
        return jsonify(success=False, error="There was a problem adding the item into the cart")
    return jsonify(success=True, message="Item successfully added to cart")

@app.route('/get_shopping_cart', methods=['POST'])
def get_shopping_cart():
    email = json.loads(str(request.data, "utf-8"))['email']
    return jsonify(get_shopping_cart_data(email))

@app.route('/delete_from_cart', methods=['POST'])
def remove_from_cart():
    data = json.loads(str(request.data, "utf-8"))
    email = data['email']
    ret = delete_from_shopping_cart(data, email)
    if (not ret):
        return jsonify(success=ret, message="There was a problem trying to remove this item from cart")
    return jsonify(success=ret, message="Item successfully removed from cart")

@app.route('/checkout_cart', methods=['POST'])
def checkout():
    try:
        data = json.loads(str(request.data, "utf-8"))
        ccn = data['ccn']
        billing = data['billing']
        shipping = data['shipping']
        facility = data['facility']
        email = data['email']
        checkout_info = {'ccn':ccn, 'billing':billing, 'shipping':shipping, 'facility':facility}
        ret = checkout_cart(email, checkout_info)
        if (not ret):
            return jsonify(success=ret, error="Attempting to checkout empty cart")
    except:
        return jsonify(success=False, error="Bad POST Request")
    return jsonify(success=ret, message="Checkout successful")

@app.route('/get_shipment_by_purchase_id', methods=['POST'])
def get_shipment_by_pid():
    purchaseid = json.loads(str(request.data, "utf-8"))['purchaseid']
    return jsonify(get_shipment_by_purchase_id(purchaseid))

@app.route('/make_review', methods=['POST'])
def make_review():
    try:
        data = json.loads(str(request.data, "utf-8"))
        buyer_email = data['buyer_email']
        seller_email = data['seller_email']
        item_name = data['item_name']
        feedback = data['feedback']
        score = data['score']
        review = {"buyer_email":buyer_email, "seller_email":seller_email, "item_name":item_name, "feedback":feedback, "score":score}
        ret = create_review(review)
        if (not ret):
            return jsonify(success=ret, error="There was a problem creating the review")
    except:
        return jsonify(success=False, error="Bad POST Request")
    return jsonify(success=ret, message="Review created successfully")

@app.route('/reviews_by_user', methods=['POST'])
def list_reviews_by_user():
    email = json.loads(str(request.data, "utf-8"))['email']
    return jsonify(get_reviews_user(email))

@app.route('/get_item_keyword', methods=['POST'])
def get_item_by_keyword():
    key = json.loads(str(request.data, "utf-8"))['keyword']
    return jsonify(get_item_keyword(key))

@app.route('/cards_from_user', methods=['POST'])
def get_cards_from_user():
    email = json.loads(str(request.data, "utf-8"))['email']
    return jsonify(get_cards_user(email))

@app.route('/items_by_user', methods=['POST'])
def list_items_by_user():
    email = json.loads(str(request.data, "utf-8"))['email']
    return jsonify(get_all_items_user(email))

@app.route('/delete_item_from_user', methods=['POST'])
def delete_item_from_user():
    data = json.loads(str(request.data, "utf-8"))
    ret = True
    try:
        email = data['email']
        id = data['id']
        ret = delete_item_user(email, id)
    except:
        return jsonify(success=False, error="There was a problem deleting the item from user")
    if (not ret):
        return jsonify(success=False, error="There was a problem deleting the item from user")
    return jsonify(success=True, message="Item deleted successfully")

@app.route('/item/<int:item_id>', methods=['POST'])
def display_item(item_id):
    return jsonify(get_item_by_id(item_id))

@app.route('/link_for_item', methods=['POST'])
def item_link():
    itemid = json.loads(str(request.data, "utf-8"))['id']
    return jsonify(get_link(itemid))

@app.route('/purchases_for_user', methods=['POST'])
def get_purchases_for_user():
    email = json.loads(str(request.data, "utf-8"))['email']
    return jsonify(get_purchase_user(email))

@app.route('/links', methods=['GET'])
def list_links():
    return jsonify(get_links())

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify(get_users())

@app.route('/reviews', methods=['GET'])
def list_reviews():
    return jsonify(get_reviews())

@app.route('/items', methods=['GET'])
def list_items():
    return jsonify(get_items())

@app.route('/cards', methods=['GET'])
def list_cards():
    return jsonify(get_cards())

@app.route('/purchases', methods=['GET'])
def list_purchases():
    return jsonify(get_purchases())

@app.route('/carts', methods=['GET'])
def list_carts():
    return jsonify(get_carts())

@app.route('/shipments', methods=['GET'])
def list_shipments():
    return jsonify(get_shipments())

if __name__ == '__main__':
    app.run(host='', port=8000, debug=True)
    initializedb()
