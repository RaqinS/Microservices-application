from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Order_status(Base):

    __tablename__ = "Order_status"

    id = Column(Integer, primary_key=True)
    OrderID = Column(String(50), primary_key=True)
    CustomerAdress = Column(String(100), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    OrderType = Column(String(50), nullable=False)
    RestaurantID = Column(String(50), nullable=False)
    Tip = Column(Integer, nullable=True)
    date_created = Column(DateTime, nullable=False)
    Customer_PhoneNumber = Column(Integer, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, OrderID,CustomerAdress,timestamp,OrderType,RestaurantID,Customer_PhoneNumber,Tip,trace_id):
        self.OrderID = OrderID
        self.CustomerAdress = CustomerAdress
        self.timestamp = timestamp 
        self.date_created = datetime.datetime.now()
        self.RestaurantID = RestaurantID
        self.OrderType = OrderType
        self.Customer_PhoneNumber = Customer_PhoneNumber
        self.Tip = Tip
        self.trace_id = trace_id

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['OrderID'] = self.OrderID
        dict['CustomerAdress'] = self.CustomerAdress
        dict['timestamp'] = self.timestamp
        dict['RestaurantID'] = self.RestaurantID
        dict['OrderType'] = self.OrderType
        dict['Tip'] = self.Tip
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict