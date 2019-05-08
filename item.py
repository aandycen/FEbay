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
        VALUES ({}, {}, {}, "{}", date('now', '+6 months'))
        '''.format(item['price'], sellerID, item['quantity'], item['name']))
        c.execute('''
        SELECT MAX(ItemID)
        FROM Item
        ''')
        itemID = c.fetchone()[0]
        c.execute('''
        INSERT INTO ImageLink (ItemID, Link)
        VALUES ({}, "{}")
        '''.format(itemID, item['link']))
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
        email = get_email(row[2])
        items.append({'Price':row[0],'ItemID':row[1], 'Email':email, 'SellerID':row[2],'Quantity':row[3],'Name':row[4]})
    conn.close()
    return items

def get_item_id(email, name):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    sellerID = get_userid(email)
    c.execute('''
    SELECT I.ItemID
    FROM Item I
    WHERE I.SellerID = {} AND I.Name = "{}"
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
        if (row[3] > 0):
            list_of_items.append({'Price':row[0],'ItemID':row[1],'SellerID':row[2],'Quantity':row[3],'Name':row[4]})
    conn.close()
    return list_of_items

def delete_item_user(email, id):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    userID = get_userid(email)
    try:
        # c.execute('''
        # DELETE FROM Item
        # WHERE SellerID = {} AND ItemID = {}
        # '''.format(userID, id))
        # c.execute('''
        # DELETE FROM ImageLink
        # WHERE ItemID = {}
        # '''.format(id))
        c.execute('''
        UPDATE Item
        SET Quantity = 0
        WHERE ItemId = {}
        '''.format(id))
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
        if (row[3] > 0):
            email = get_email(row[2])
            list_of_items.append({'Price':row[0],'ItemID':row[1], 'Email':email, 'SellerID':row[2],'Quantity':row[3],'Name':row[4]})
    conn.close()
    return list_of_items

def get_all_items():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Item
    ''')
    rows = c.fetchall()
    list_of_items = []
    for row in rows:
        email = get_email(row[2])
        list_of_items.append({'Price':row[0],'ItemID':row[1], 'Email':email, 'SellerID':row[2],'Quantity':row[3],'Name':row[4]})
    conn.close()
    return list_of_items

def get_links():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM ImageLink
    ''')
    rows = c.fetchall()
    image_links = []
    for row in rows:
        image_links.append({'ImageLinkID':row[0],'ItemID':row[1],'Link':row[2]})
    conn.close()
    return image_links

def get_link(id):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    link = None
    try:
        c.execute('''
        SELECT Link FROM ImageLink
        WHERE ItemID = {}
        '''.format(id))
        link = c.fetchone()[0]
    except sqlite3.Error as e:
        print("Database error: %s" % e)
    finally:
        return link

def get_items_sorted_by_price(order):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Item
    ORDER BY Price {}
    '''.format(order))
    rows = c.fetchall()
    list_of_items = []
    for row in rows:
        if (row[3] > 0):
            email = get_email(row[2])
            list_of_items.append({'Price':row[0],'ItemID':row[1], 'Email':email, 'SellerID':row[2],'Quantity':row[3],'Name':row[4]})
    conn.close()
    return list_of_items

def get_items_sorted_by_quantity(order):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Item
    ORDER BY Quantity {}
    '''.format(order))
    rows = c.fetchall()
    list_of_items = []
    for row in rows:
        if (row[3] > 0):
            email = get_email(row[2])
            list_of_items.append({'Price':row[0],'ItemID':row[1], 'Email':email, 'SellerID':row[2],'Quantity':row[3],'Name':row[4]})
    conn.close()
    return list_of_items

def get_items_sorted_by_user_rating(order):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT U.UserID, U.Rating
    FROM User U
    ORDER BY U.Rating {}
    '''.format(order))
    users = c.fetchall()
    list_of_items = []
    for user in users:
        users_items = get_all_items_user(get_email(user[0]))
        for item in users_items:
            email = get_email(item['SellerID'])
            link = get_link(item['ItemID'])
            list_of_items.append({'Rating':user[1], 'Price':item['Price'],'ItemID':item['ItemID'],
            'Email':email, 'SellerID':item['SellerID'],'Quantity':item['Quantity'],'Name':item['Name'], "link":link})
    conn.close()
    return list_of_items
