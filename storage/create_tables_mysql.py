import mysql.connector

# Establish a connection to the MySQL database
db_conn = mysql.connector.connect(
    host="ec2-3-133-144-150.us-east-2.compute.amazonaws.com",
    user="user",
    password="password",
    database="events"
)
db_cursor = db_conn.cursor()

# Create the 'Order_status' table with trace_id
db_cursor.execute('''
CREATE TABLE Order_status (
    id INT NOT NULL AUTO_INCREMENT,
    OrderID VARCHAR(50) NOT NULL,
    CustomerAdress VARCHAR(100) NOT NULL,
    timestamp VARCHAR(100) NOT NULL,
    OrderType VARCHAR(50) NOT NULL,
    RestaurantID VARCHAR(50) NOT NULL,
    Tip INT,
    date_created VARCHAR(100) NOT NULL,
    Customer_PhoneNumber VARCHAR(50) NOT NULL,
    trace_id VARCHAR(250) NOT NULL,
    CONSTRAINT Order_status_pk PRIMARY KEY(id)              
)
''')

# Create the 'OrderETA' table with trace_id
db_cursor.execute('''
CREATE TABLE OrderETA (
    id INT NOT NULL AUTO_INCREMENT,
    OrderID INT NOT NULL,
    CustomerLatitude INT NOT NULL,
    CustomerLongitude INT NOT NULL,
    DriverLatitude INT NOT NULL,
    DriverLongitude INT NOT NULL,
    RestaurantLatitude INT NOT NULL,
    RestaurantLongitude INT NOT NULL,
    OrderType VARCHAR(50) NOT NULL,
    Distance INT NOT NULL,
    date_created VARCHAR(100) NOT NULL,
    timestamp VARCHAR(100) NOT NULL,
    trace_id VARCHAR(250) NOT NULL,
    CONSTRAINT Order_status_pk PRIMARY KEY(id)              
)
''')

# Commit the changes to the database and close the connection
db_conn.commit()
db_conn.close()
