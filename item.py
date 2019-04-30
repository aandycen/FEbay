from database import *
import sqlite3

def create_item(email, item):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    sellerID = get_userid(email)
    try:
        c.execute('''
        INSERT INTO Item (Price, SellerID, Quantity, Name, DateOutOfStock)
        VALUES ({}, {}, {}, '{}', date('now', '+6 months'))
        '''.format(item['price'], sellerID, item['quantity'], item['name']))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def get_all_items():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Item
    ''')
    rows = c.fetchall()
    list_of_items = []
    for row in rows:
        list_of_items.append({'Price':row[0],'ItemID':row[1],'SellerID':row[2],'Quantity':row[3],'Name':row[4],
        'DateOutOfStock':row[5]})
    conn.close()
    return list_of_items

def get_all_items_user(email):
    userID = get_userid(email)
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Item
    WHERE SellerID = {}
    '''.format(userID))
    rows = c.fetchall()
    list_of_items = []
    for row in rows:
        list_of_items.append({'Price':row[0],'ItemID':row[1],'SellerID':row[2],'Quantity':row[3],'Name':row[4],
        'DateOutOfStock':row[5]})
    conn.close()
    return list_of_items

def delete_item_user(email, id):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    userID = get_userid(email)
    try:
        c.execute('''
        DELETE FROM Item
        Where SellerID = {} AND ItemID = {}
        '''.format(userID, id))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def get_purchases(email):
    userID = get_userid(email)
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Purchase
    WHERE BuyerID = {}
    '''.format(userID))
    rows = c.fetchall()
    purchases = []
    for row in rows:
        purchases.append({'PurchaseID':row[0],'ShoppingCartID':row[1],'CCN':row[2],'Price':row[3],'OrderDate':row[4],
        'Billing':row[5], "Shipping":row[6], "BuyerID":row[7]})
    conn.close()
    return purchases
