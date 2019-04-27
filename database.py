import sqlite3

def register_user(acct):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    success = True
    try:
        c.execute('''
        INSERT INTO User (FirstName, LastName, Email, Password, Rating, DateJoined)
        VALUES ({}, {}, {}, {}, 0, GETDATE())
        '''.format(acct['first'], acct['last'], acct['email'], acct['password']))
        conn.commit()
    except:
        conn.rollback()
        success = False
    finally:
        return success

def login_user(email, password):
    conn = sqlite3.connect('cse305.db')
    c = conn.cursor()
    try:
        c.execute('''
        SELECT U.FirstName, U.LastName
        FROM User U
        WHERE U.Email = {} AND U.Password = {}
        '''.format(email, password))
        return c.fetchone()
    except:
        return None

# also update billing address since the two are directly related
def update_credit_card():
    return None

def update_shipping():
    return None

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
