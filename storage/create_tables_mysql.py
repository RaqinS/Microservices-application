import mysql.connector

# Establish a connection to the MySQL database
db_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ninja462",
    database="events"
)
db_cursor = db_conn.cursor()

# Create the 'Order_status' table with trace_id
db_cursor.execute('''
CREATE TABLE Order_status (
    OrderID VARCHAR(50) NOT NULL,
    CustomerAdress VARCHAR(100) NOT NULL,
    TimeStamp VARCHAR(100) NOT NULL,
    OrderType VARCHAR(50) NOT NULL,
    RestaurantID VARCHAR(50) NOT NULL,
    Tip INT,
    Customer_PhoneNumber VARCHAR(50) NOT NULL,
    date_created VARCHAR(100) NOT NULL,
    CONSTRAINT Order_status_pk PRIMARY KEY(OrderID)              
)
''')

# Create the 'OrderETA' table with trace_id
db_cursor.execute('''
CREATE TABLE OrderETA (
    OrderID INT NOT NULL AUTO_INCREMENT,
    CustomerLatitude INT NOT NULL,
    CustomerLongitude INT NOT NULL,
    DriverLatitude INT NOT NULL,
    DriverLongitude INT NOT NULL,
    RestaurantLatitude INT NOT NULL,
    RestaurantLongitude INT NOT NULL,
    OrderType VARCHAR(50) NOT NULL,
    Distance INT NOT NULL,
    TimeStamp VARCHAR(100) NOT NULL,
    date_created VARCHAR(100) NOT NULL,
    CONSTRAINT Order_status_pk PRIMARY KEY(OrderID)              
)
''')

# Commit the changes to the database and close the connection
db_conn.commit()
db_conn.close()
