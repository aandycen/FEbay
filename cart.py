from database import *
import sqlite3
from datetime import datetime
import random

def checkout_cart(email, info):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    userID = get_userid(email)
    time = datetime.now()
    price = get_shopping_cart_data(email)['total'] + 15
    trackingNumber = ""
    for x in range(10):
        trackingNumber += str(random.randint(1,50))
    try:
        c.execute('''
        SELECT * FROM ShoppingCart
        WHERE UserID = {} and Purchased = 0
        '''.format(userID))
        cart = c.fetchall()
        if (cart == []):
            conn.close()
            return False
        # for every item in cart
        for row in cart:
            # get current quantity of item
            c.execute('''
            SELECT I.Quantity
            FROM Item I
            WHERE I.ItemID = {}
            '''.format(row[2]))
            # new quantity is current - (how many is being bought)
            quantity = c.fetchone()[0] - row[3]
            # update item in database
            c.execute('''
            UPDATE Item
            SET Quantity = {}
            WHERE ItemID = {}
            '''.format(quantity, row[2]))
            # update cart to purchased
            c.execute('''
            UPDATE ShoppingCart
            SET Purchased = 1, PurchaseDate = '{}'
            WHERE ShoppingCartID = {} AND Purchased = 0
            '''.format(time, userID))
        # create a purchase for this cart
        c.execute('''
        INSERT INTO Purchase (ShoppingCartID, CCN, Price, OrderDate, BillingAddress, ShippingAddress, BuyerID)
        VALUES ({}, {}, {}, '{}', '{}', '{}', {})
        '''.format(cart[0][0], info['ccn'], price, time, info['billing'], info['shipping'], userID))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    if (success == False):
        conn.close()
        return success
    try:
        conn = sqlite3.connect('cse305.db')
        c = conn.cursor()
        # get this purchase id
        c.execute('''
        SELECT P.PurchaseID
        FROM Purchase P
        WHERE ShoppingCartID = {} AND OrderDate = '{}' AND BuyerID = {}
        '''.format(userID, time, userID))
        id = c.fetchone()[0]
        # create a shipment for this purchase
        c.execute('''
        INSERT INTO Shipment (TrackingNumber, Status, Facility, DeliveryDate, PurchaseID)
        VALUES ({}, {}, '{}', date('now', '+7 days'), {})
        '''.format(trackingNumber, 0, info['facility'], id))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def update_shopping_cart(item, email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    userID = get_userid(email)
    try:
        c.execute('''
        UPDATE ShoppingCart
        SET ItemQuantity = {}
        WHERE UserID = {} AND ItemID = {} AND Purchased = 0
        '''.format(item['quantity'], userID, item['id']))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def delete_from_shopping_cart(item, email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    userID = get_userid(email)
    try:
        c.execute('''
        DELETE FROM ShoppingCart
        Where UserID = {} AND ItemID = {} AND Purchased = 0
        '''.format(userID, item['id']))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def get_shopping_cart_data(email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    userID = get_userid(email)
    items = []
    subtotal = 0
    try:
        c.execute('''
        SELECT * FROM ShoppingCart
        WHERE UserID = {} and Purchased = 0
        '''.format(userID))
        cart = c.fetchall()
        for entry in cart:
            c.execute('''
            SELECT I.Name, I.Price, I.SellerID, I.Quantity
            FROM Item I
            WHERE I.ItemID = {}
            '''.format(entry[2]))
            item = c.fetchone()
            seller_email = get_email(item[2])
            items.append({'in_stock': item[3], 'seller':seller_email, 'itemid':entry[2], 'name':item[0], 'quantity':entry[3], 'price':item[1] * entry[3]})
            subtotal += item[1] * entry[3]
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return {'items':items, 'total':subtotal, 'success':success}

def add_to_shopping_cart(item, email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    userID = get_userid(email)
    try:
        c.execute('''
        SELECT I.Quantity, I.SellerID
        FROM Item I
        WHERE I.ItemID = {}
        '''.format(item['id']))
        data = c.fetchone()
        quantity = data[0]
        sellerID = data[1]
        if (sellerID == userID):
            conn.close()
            success = False
        if (item['quantity'] > quantity or item['quantity'] <= 0):
            conn.close()
            success = False
        current_cart = get_shopping_cart_data(email)
        current_items = current_cart['items']
        for i in current_items:
            if (item['id'] == i['itemid']):
                update_shopping_cart({'quantity':item['quantity'], 'id':item['id']}, email)
                conn.close()
        c.execute('''
        INSERT INTO ShoppingCart(ShoppingCartID, UserID, ItemID, ItemQuantity) VALUES ({}, {}, {}, {})
        '''.format(userID, userID, item['id'], item['quantity']))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def get_carts():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM ShoppingCart
    ''')
    rows = c.fetchall()
    carts = []
    for row in rows:
        email = get_email(row[1])
        carts.append({'ShoppingCartID':row[0], 'Email':email, 'UserID':row[1],'ItemID':row[2],'ItemQuantity':row[3],'Purchased':row[4], 'PurchaseDate':row[5]})
    conn.close()
    return carts
