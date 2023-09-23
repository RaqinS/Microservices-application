from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class OrderETA(Base):

    __tablename__ = "OrderETA"

    OrderID = Column(Integer, primary_key=True)
    CustomerLatitude = Column(Integer, nullable=False)
    CustomerLongitude = Column(Integer, nullable=False)
    RestaurantLatitude = Column(Integer, nullable=False)
    RestaurantLongitude = Column(Integer, nullable=False)
    DriverLatitude = Column(Integer, nullable=False)
    OrderType = Column(String(50), nullable=False)
    DriverLongitude = Column(Integer, nullable=False)
    Distance = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, OrderID,CustomerLatitude,CustomerLongitude,RestaurantLatitude,RestaurantLongitude,DriverLatitude,DriverLongitude,OrderType,Distance):
        self.OrderID = OrderID
        self.CustomerLatitude = CustomerLatitude
        self.CustomerLongitude = CustomerLongitude
        self.date_created = datetime.datetime.now() 
        self.DriverLatitude = DriverLatitude
        self.DriverLongitude = DriverLongitude
        self.Distance = Distance
        self.OrderType = OrderType
        self.RestaurantLatitude = RestaurantLatitude
        self.RestaurantLongitude = RestaurantLongitude

    def to_dict(self):
        dict = {}
        dict['CustomerLatitude'] = self.CustomerLatitude
        dict['CustomerLongitude'] = self.CustomerLongitude
        dict['DriverLatitude'] = self.DriverLatitude
        dict['DriverLongitude'] = self.DriverLongitude
        dict['RestaurantLatitude'] = self.RestaurantLatitude
        dict['RestaurantLongitude'] = self.RestaurantLongitude
        dict['date_created'] = self.date_created
        dict['Distance'] = self.Distance
        dict['OrderType'] = self.OrderType
        