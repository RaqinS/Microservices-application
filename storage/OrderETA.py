from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class OrderETA(Base):

    __tablename__ = "OrderETA"

    id = Column(Integer, primary_key=True)
    OrderID = Column(Integer, nullable=False)
    CustomerLatitude = Column(Integer, nullable=False)
    CustomerLongitude = Column(Integer, nullable=False)
    RestaurantLatitude = Column(Integer, nullable=False)
    RestaurantLongitude = Column(Integer, nullable=False)
    DriverLatitude = Column(Integer, nullable=False)
    OrderType = Column(String(50), nullable=False)
    DriverLongitude = Column(Integer, nullable=False)
    Distance = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, OrderID,CustomerLatitude,CustomerLongitude,RestaurantLatitude,RestaurantLongitude,DriverLatitude,DriverLongitude,OrderType,Distance,timestamp,trace_id):
        self.OrderID = OrderID
        self.CustomerLatitude = CustomerLatitude
        self.CustomerLongitude = CustomerLongitude
        self.DriverLatitude = DriverLatitude
        self.DriverLongitude = DriverLongitude
        self.Distance = Distance
        self.OrderType = OrderType
        self.RestaurantLatitude = RestaurantLatitude
        self.RestaurantLongitude = RestaurantLongitude
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        self.trace_id = trace_id
    
    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['OrderID'] = self.OrderID
        dict['CustomerLatitude'] = self.CustomerLatitude
        dict['CustomerLongitude'] = self.CustomerLongitude
        dict['DriverLatitude'] = self.DriverLatitude
        dict['DriverLongitude'] = self.DriverLongitude
        dict['RestaurantLatitude'] = self.RestaurantLatitude
        dict['RestaurantLongitude'] = self.RestaurantLongitude
        dict['Distance'] = self.Distance
        dict['OrderType'] = self.OrderType
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id
        return dict