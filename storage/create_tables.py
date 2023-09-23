import sqlite3

conn = sqlite3.connect('readings.sqlite')



c = conn.cursor()



c.execute('''
          CREATE TABLE Order_status
          (OrderID VARCHAR(50) PRIMARY KEY,
          CustomerAdress VARCHAR(100) NOT NULL,
          TimeStamp VARCHAR(100) NOT NULL,
          OrderType VARCHAR(50) NOT NULL,
          RestaurantID VARCHAR(50) NOT NULL,
          Tip INTEGER,
          Customer_PhoneNumber INTEGER NOT NULL,
          date_created VARCHAR(100) NOT NULL)
        '''
)

c.execute('''
    CREATE TABLE OrderETA
    (OrderID INTEGER PRIMARY KEY,
    CustomerLatitude INTEGER NOT NULL,
    CustomerLongitude INTEGER NOT NULL,
    DriverLatitude INTEGER NOT NULL,
    DriverLongitude INTEGER NOT NULL,
    RestaurantLatitude INTEGER NOT NULL,
    RestaurantLongitude INTEGER NOT NULL,
    OrderType VARCHAR(50) NOT NULL,
    Distance INTEGER NOT NULL,
    date_created VARCHAR(100) NOT NULL)
''')

conn.commit()
conn.close()