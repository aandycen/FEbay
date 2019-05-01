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
    row = {}
    try:
        c.execute('''
        SELECT U.FirstName, U.LastName
        FROM User U
        WHERE U.Email = \'{}\' AND U.Password = '{}'
        '''.format(email, password))
        data = c.fetchone()
        row = {'FirstName':data[0], 'LastName':data[1]}
    except sqlite3.Error as e:
        print("Database error: %s" % e)
    finally:
        conn.close()
        return row

def get_user(email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM User
    WHERE Email = \'{}\'
    '''.format(email))
    user = c.fetchone()
    user_data = {"UserID":user[0],"FirstName":user[1],
    "LastName":user[2],"Email":user[3],"Password":user[4],
    "Rating":user[5],"Billing":user[6],"Shipping":user[7],"DateJoined":user[8]}
    conn.close()
    return user_data

def update_password(password, email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    userID = get_userid(email)
    try:
        c.execute('''
        UPDATE User
        SET Password = '{}'
        WHERE Email = \'{}\'
        '''.format(password, email))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
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
    except sqlite3.Error as e:
        print("Database error: %s" % e)
        conn.rollback()
        success = False
    finally:
        conn.close()
        return success

def get_userid(email):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    userID = None
    try:
        c.execute('''
        SELECT U.UserID
        FROM User U
        Where U.Email = \'{}\'
        '''.format(email))
        userID = c.fetchone()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
    finally:
        conn.close()
        if (userID):
            return userID[0]
        return None

def get_users():
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM User
    ''')
    rows = c.fetchall()
    list_of_users = []
    for row in rows:
        list_of_users.append({'UserID':row[0],'FirstName':row[1],'LastName':row[2],'Email':row[3],'Password':row[4],
        'Rating':row[5],'Billing':row[6], 'Shipping':row[7], 'DateJoined':row[8]})
    conn.close()
    return list_of_users

def get_table(table_name):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    table = None
    try:
        c.execute('''
        SELECT * FROM {}
        '''.format(table_name))
        table = c.fetchall()
    except sqlite3.Error as e:
        print("Database error: %s" % e)
    finally:
        conn.close()
        return table

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
    PRIMARY KEY (ReviewID),
    FOREIGN KEY (SellerID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (SellerID) REFERENCES Item(SellerID) ON DELETE CASCADE,
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
    PRIMARY KEY (ItemID),
    FOREIGN KEY (SellerID) REFERENCES User(UserID) ON DELETE CASCADE,
    CHECK (Price > 0)
    );
    ''')

    c.execute('''CREATE TABLE if not exists ShoppingCart (
    ShoppingCartID Integer NOT NULL,
    UserID Integer NOT NULL,
    ItemID Integer NOT NULL,
    ItemQuantity Integer NOT NULL,
    Purchased Integer DEFAULT 0,
    PurchaseDate DATETIME DEFAULT NULL,
    PRIMARY KEY (ShoppingCartID, ItemID, Purchased),
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID) ON DELETE CASCADE
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
    ShoppingCartID Integer NOT NULL,
    CCN Integer NOT NULL,
    Price FLOAT(10,2) NOT NULL,
    OrderDate DATETIME NOT NULL,
    BillingAddress VARCHAR(50) NOT NULL,
    ShippingAddress VARCHAR(50) NOT NULL,
    BuyerID Integer NOT NULL,
    PRIMARY KEY(PurchaseID),
    FOREIGN KEY (BuyerID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (CCN) REFERENCES CreditCard(CCN) ON DELETE CASCADE,
    FOREIGN KEY (ShoppingCartID) REFERENCES ShoppingCart(ShoppingCartID) ON DELETE CASCADE,
    FOREIGN KEY (OrderDate) REFERENCES ShoppingCart(PurchaseDate) ON DELETE CASCADE
    );
    ''')

    c.execute('''CREATE TABLE if not exists Shipment (
    ShipmentID Integer NOT NULL,
    TrackingNumber Integer NOT NULL,
    Status Integer DEFAULT 0,
    Facility VARCHAR(50) NOT NULL,
    DeliveryDate DATETIME NOT NULL,
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

    return
