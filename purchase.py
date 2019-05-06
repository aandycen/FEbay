from database import *
import sqlite3

def get_purchase_user(email):
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
        items = []
        c.execute('''
        SELECT C.ItemID, C.ItemQuantity
        FROM ShoppingCart C
        WHERE C.PurchaseDate = "{}"
        '''.format(row[4]))
        for item in c.fetchall():
            c.execute('''
            SELECT I.Name, I.SellerID
            FROM Item I
            WHERE I.ItemID = {}
            '''.format(item[0]))
            data = c.fetchone()
            item_name = data[0]
            seller_email = get_email(data[1])
            quantity = item[1]
            items.append({'item':item_name, 'seller':seller_email, 'quantity':quantity})
        purchases.append({'PurchaseID':row[0],'ShoppingCartID':row[1],'CCN':row[2],'Price':row[3],'OrderDate':row[4],
        'Billing':row[5], "Shipping":row[6], "BuyerID":row[7], 'Items':items})
    conn.close()
    return purchases

def get_purchases():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Purchase
    ''')
    rows = c.fetchall()
    purchases = []
    for row in rows:
        items = []
        c.execute('''
        SELECT C.ItemID, C.ItemQuantity
        FROM ShoppingCart C
        WHERE C.PurchaseDate = "{}"
        '''.format(row[4]))
        for item in c.fetchall():
            c.execute('''
            SELECT I.Name, I.SellerID
            FROM Item I
            WHERE I.ItemID = {}
            '''.format(item[0]))
            data = c.fetchone()
            item_name = data[0]
            seller_email = get_email(data[1])
            quantity = item[1]
            items.append({'item':item_name, 'seller':seller_email, 'quantity':quantity})
        email = get_email(row[7])
        purchases.append({'PurchaseID':row[0],'ShoppingCartID':row[1],'CCN':row[2],'Price':row[3],'OrderDate':row[4],
        'BillingAddress':row[5],'ShippingAddress':row[6],'BuyerID':row[7], 'Email': email, "Items":items})
    conn.close()
    return purchases

def get_shipments():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Shipment
    ''')
    rows = c.fetchall()
    shipments = []
    for row in rows:
        shipments.append({'ShipmentID':row[0],'TrackingNumber':row[1],'Status':row[2],'Facility':row[3],'DeliveryDate':row[4],'PurchaseID':row[5]})
    conn.close()
    return shipments

def get_shipment_by_purchase_id(id):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM Shipment
    WHERE PurchaseID = {}
    '''.format(id))
    row = c.fetchone()
    shipment = {'ShipmentID':row[0],'TrackingNumber':row[1],'Status':row[2],'Facility':row[3],'DeliveryDate':row[4],'PurchaseID':row[5]}
    conn.close()
    return shipment
