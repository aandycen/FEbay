from database import *
import sqlite3

def create_review(review):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    buyerID = get_userid(review['buyer_email'])
    sellerID = get_userid(review['seller_email'])
    if (buyerID == None or sellerID == None):
        conn.close()
        return False
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
        if success:
            return update_user_rating(sellerID)
        return success

def update_user_rating(sellerID):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    num_reviews = 0
    score = 0
    try:
        c.execute('''
        SELECT COUNT(*)
        FROM Review
        WHERE SellerID = {}
        '''.format(sellerID))
        num_reviews = c.fetchone()[0]
        c.execute('''
        SELECT R.Score
        FROM Review R
        WHERE R.SellerID = {}
        '''.format(sellerID))
        reviews = c.fetchall()
        for review in reviews:
            score += review[0]
        score /= num_reviews
        c.execute('''
        UPDATE User
        SET Rating = {}
        WHERE UserID = {}
        '''.format(score, sellerID))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def get_reviews_user(email):
    conn = sqlite3.connect('cse305.db')
    userID = get_userid(email)
    if (userID == None):
        conn.close()
        return []
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Review
    WHERE SellerID = {}
    '''.format(userID))
    rows = c.fetchall()
    reviews = []
    for row in rows:
        bemail = get_email(row[5])
        semail = get_email(row[2])
        reviews.append({'ReviewID':row[0],'DateWritten':row[1],'SellerID':row[2],'Feedback':row[3],'ItemName':row[4],
        'BuyerID':row[5], "Score":row[6], 'SellerEmail':semail, 'BuyerEmail':bemail})
    conn.close()
    return reviews

def get_reviews():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Review
    ''')
    rows = c.fetchall()
    reviews = []
    for row in rows:
        bemail = get_email(row[5])
        semail = get_email(row[2])
        reviews.append({'ReviewID':row[0],'DateWritten':row[1],'SellerID':row[2],'Feedback':row[3],'ItemName':row[4],
        'BuyerID':row[5], "Score":row[6], 'SellerEmail':semail, 'BuyerEmail':bemail})
    conn.close()
    return reviews
