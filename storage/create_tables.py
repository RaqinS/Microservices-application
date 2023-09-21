import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          Create TABLE Order_status
          (OrderID VARCHAR(50) PRIMARY KEY,
          CustomerAdress VARCHAR(100) NOT NULL,
          TimeStamp VARCHAR(100) NOT NULL,
          OrderType VARCHAR(50) NOT NULL,
          RestaurantID VARCHAR(50) NOT NULL,
          Tip INTEGER NOT NULL,
          Customer_PhoneNumber INTEGER NOT NULL
          )
        '''
          )


c.execute('''
          Create TABLE OrderETA
          (OrderID INTEGER NOT NULL,
          CustomerLatitude INTEGER NOT NULL,
          CustomerLongitude INTEGER NOT NULL,
          DriverLatitude INTEGER NOT NULL,
          DriverLongitude INTEGER NOT NULL,
          RestaurantLatitude INTEGER NOT NULL,
          RestaurantLongitude INTEGER NOT NULL,
          OrderType VARCHAR(50) NOT NULL,
          Distance INTEGER NOT NULL,
          FOREIGN KEY (OrderID) REFERENCES Order_status(OrderID)
          )
        '''
          )

conn.commit()
conn.close()