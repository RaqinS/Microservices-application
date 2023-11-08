import mysql.connector

# Establish a connection to the MySQL database
db_conn = mysql.connector.connect(
    host="ec2-18-219-137-169.us-east-2.compute.amazonaws.com",
    user="user",
    password="password",
    database="events"
)
db_cursor = db_conn.cursor()

# Drop the 'Order_status' table if it exists
db_cursor.execute('''
DROP TABLE IF EXISTS Order_status;
''')

# Drop the 'OrderETA' table if it exists
db_cursor.execute('''
DROP TABLE IF EXISTS OrderETA;
''')

# Commit the changes to the database and close the connection
db_conn.commit()
db_conn.close()

print("Tables dropped successfully.")
