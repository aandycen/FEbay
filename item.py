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
