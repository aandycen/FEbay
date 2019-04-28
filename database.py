import sqlite3

def register_user(acct):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    try:
        c.execute('''
        INSERT INTO User (FirstName, LastName, Email, Password, Rating, DateJoined)
        VALUES ('{}', '{}', \'{}\', '{}', 0, date('now'))
        '''.format(acct['first'], acct['last'], acct['email'], acct['password']))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def login_user(email, password):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    row = None
    try:
        c.execute('''
        SELECT U.FirstName, U.LastName
        FROM User U
        WHERE U.Email = \'{}\' AND U.Password = '{}'
        '''.format(email, password))
        row = c.fetchone()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
    finally:
        conn.close()
        return row

def add_credit_card(card, email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    userID = get_userid(email)
    try:
        c.execute('''
        INSERT INTO CreditCard(UserID, CCN, SecurityCode, ExpiryDate) VALUES ({}, '{}', '{}', '{}')
        '''.format(userID, card['ccn'], card['securitycode'], card['expirydate']))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        return success

def update_shipping(address, email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    try:
        c.execute('''
        UPDATE User
        SET ShippingAddress = '{}'
        WHERE Email = \'{}\'
        '''.format(address, email))
        conn.commit()
        return "Success"
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def update_billing(address, email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    try:
        c.execute('''
        UPDATE User
        SET BillingAddress = '{}'
        WHERE Email = \'{}\'
        '''.format(address, email))
        conn.commit()
        return "Success"
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def create_item(email, item):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    sellerID = get_userod(email)
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

def create_review(review):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    buyerID = get_userid(review['buyer_email'])
    sellerID = get_userid(review['seller_email'])
    try:
        c.execute('''
        INSERT INTO Review (DateWritten, SellerID, Feedback, ItemName, BuyerID, Score)
        VALUES (date('now'), {}, '{}', '{}', {}, {}))
        '''.format(sellerID, review['feedback'], review['item_name'], buyerID, review['score']))))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def get_userid(email):
    return c.execute('''
    SELECT U.UserID
    FROM User U
    Where U.Email = \'{}\'
    '''.format(email))

def initializedb():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists User (
    UserID Integer DEFAULT AUTO_INCREMENT,
    FirstName VARCHAR(20) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    Email VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(50) NOT NULL,
    Rating FLOAT DEFAULT 0,
    BillingAddress VARCHAR(50) DEFAULT NULL,
    ShippingAddress VARCHAR(50) DEFAULT NULL,
    DateJoined DATETIME,
    PRIMARY KEY (UserID),
    CHECK (Email LIKE '%@%'),
    CHECK (LENGTH(Password) >= 8)
    );
    ''')

    c.execute('''CREATE TABLE if not exists Review (
    ReviewID Integer DEFAULT AUTO_INCREMENT,
    DateWritten DATETIME,
    SellerID Integer NOT NULL,
    Feedback VARCHAR(255) DEFAULT ‘’,
    ItemName  VARCHAR(50) NOT NULL,
    BuyerID Integer NOT NULL,
    Score Integer NOT NULL,
    PRIMARY KEY (BuyerID, ReviewID),
    FOREIGN KEY (SellerID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (BuyerID) REFERENCES User(UserID) ON DELETE CASCADE,
    CHECK (Score BETWEEN 1 and 5),
    CHECK (SellerID != BuyerID)
    );
    ''')

    c.execute('''CREATE TABLE if not exists Item (
    Price FLOAT(10,2) NOT NULL,
    ItemID Integer DEFAULT AUTO_INCREMENT,
    SellerID Integer NOT NULL,
    Quantity Integer NOT NULL,
    Name VARCHAR(50) NOT NULL,
    DateOutOfStock DATETIME DEFAULT NULL,
    PRIMARY KEY (ItemID, SellerID),
    FOREIGN KEY (SellerID) REFERENCES User(UserID) ON DELETE CASCADE,
    CHECK (Price > 0)
    );
    ''')

    c.execute('''CREATE TABLE if not exists ShoppingCart (
    ShoppingCartID Integer NOT NULL,
    UserID Integer NOT NULL,
    ItemID Integer NOT NULL,
    ItemQuantity Integer NOT NULL,
    Purchased Boolean DEFAULT false,
    PRIMARY KEY (ShoppingCartID, ItemID),
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY(ItemID) REFERENCES Item(ItemID) ON DELETE CASCADE
    );
    ''')

    c.execute('''CREATE TABLE if not exists CreditCard (
    UserID Integer NOT NULL,
    CCN Integer(16) NOT NULL,
    SecurityCode Integer(3) NOT NULL,
    ExpiryDate DATETIME NOT NULL,
    PRIMARY KEY (UserID, CCN),
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
    );
    ''')

    c.execute('''CREATE TABLE if not exists Purchase (
    PurchaseID Integer DEFAULT AUTO_INCREMENT,
    ShoppingCart Integer NOT NULL,
    CCN Integer NOT NULL,
    Price FLOAT(10,2) NOT NULL,
    OrderDate DATETIME NOT NULL,
    BillingAddress VARCHAR(50) NOT NULL,
    ShippingAddress VARCHAR(50) NOT NULL,
    BuyerID Integer NOT NULL,
    PRIMARY KEY(PurchaseID),
    FOREIGN KEY (BuyerID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (CCN) REFERENCES CreditCard(CCN) ON DELETE CASCADE,
    FOREIGN KEY (ShoppingCart) REFERENCES ShoppingCart(ShoppingID) ON DELETE CASCADE
    );
    ''')

    c.execute('''CREATE TABLE if not exists Shipment (
    ShipmentID Integer NOT NULL,
    TrackingNumber Integer NOT NULL,
    Status Integer DEFAULT 0,
    Facility VARCHAR(50) NOT NULL,
    DeliveryDate VARCHAR(8) NOT NULL,
    PurchaseID Integer NOT NULL,
    PRIMARY KEY (ShipmentID),
    FOREIGN KEY (PurchaseID) REFERENCES Purchase(PurchaseID) ON DELETE CASCADE
    );
    ''')

    c.execute('''CREATE TABLE if not exists Employee (
    SupervisorID Integer DEFAULT NULL,
    ReportsTo Integer DEFAULT NULL,
    FirstName VARCHAR(20) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    Address VARCHAR(50) NOT NULL,
    SSN CHAR(9) NOT NULL,
    Salary INTEGER NOT NULL,
    PRIMARY KEY (SSN),
    FOREIGN KEY (ReportsTo) REFERENCES Employee(SupervisorID) ON DELETE CASCADE
    );
    ''')

    conn.commit()
    conn.close()
