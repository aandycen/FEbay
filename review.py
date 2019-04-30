from database import *
import sqlite3

def create_review(review):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    buyerID = get_userid(review['buyer_email'])
    sellerID = get_userid(review['seller_email'])
    try:
        c.execute('''
        INSERT INTO Review (DateWritten, SellerID, Feedback, ItemName, BuyerID, Score)
        VALUES (date('now'), {}, '{}', '{}', {}, {})
        '''.format(sellerID, review['feedback'], review['item_name'], buyerID, review['score']))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success
