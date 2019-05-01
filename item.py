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

def get_item_keyword(word):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Item
    WHERE Name LIKE '%{}%'
    '''.format(word))
    rows = c.fetchall()
    items = []
    for row in rows:
        items.append({'Price':row[0],'ItemID':row[1],'SellerID':row[2],'Quantity':row[3],'Name':row[4]})
    conn.close()
    return items

def get_item_id(email, name):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    sellerID = get_userid(email)
    c.execute('''
    SELECT I.ItemID
    FROM Item I
    WHERE I.SellerID = {} AND I.Name = '{}'
    '''.format(sellerID, name))
    itemID = c.fetchone()
    conn.close()
    return itemID[0]

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
        list_of_items.append({'Price':row[0],'ItemID':row[1],'SellerID':row[2],'Quantity':row[3],'Name':row[4]})
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

def get_item_by_id(id):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    item = None
    try:
        c.execute('''
        SELECT * FROM Item
        WHERE ItemID = {}
        '''.format(id))
        row = c.fetchone()
        item = {'Price':row[0],'ItemID':row[1],'SellerID':row[2],'Quantity':row[3],'Name':row[4]}
    except sqlite3.Error as e:
        print("Database error: %s" % e)
    finally:
        return item

def get_items():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Item
    ''')
    rows = c.fetchall()
    list_of_items = []
    for row in rows:
        list_of_items.append({'Price':row[0],'ItemID':row[1],'SellerID':row[2],'Quantity':row[3],'Name':row[4]})
    conn.close()
    return list_of_items
