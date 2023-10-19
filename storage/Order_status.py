from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Order_status(Base):

    __tablename__ = "Order_status"

    OrderID = Column(String(50), primary_key=True)
    CustomerAdress = Column(String(100), nullable=False)
    TimeStamp = Column(DateTime, nullable=False)
    OrderType = Column(String(50), nullable=False)
    RestaurantID = Column(String(50), nullable=False)
    Tip = Column(Integer, nullable=True)
    Customer_PhoneNumber = Column(Integer, nullable=False)

    def __init__(self, OrderID,CustomerAdress,TimeStamp,OrderType,RestaurantID,Customer_PhoneNumber,Tip):
        self.OrderID = OrderID
        self.CustomerAdress = CustomerAdress
        self.TimeStamp = TimeStamp 
        self.RestaurantID = RestaurantID
        self.OrderType = OrderType
        self.Customer_PhoneNumber = Customer_PhoneNumber
        self.Tip = Tip

    def to_dict(self):
        dict = {}
        dict['OrderID'] = self.OrderID
        dict['CustomerAdress'] = self.CustomerAdress
        dict['TimeStamp'] = self.TimeStamp
        dict['RestaurantID'] = self.RestaurantID
        dict['OrderType'] = self.OrderType
        dict['Tip'] = self.Tip
        dict['Customer_PhoneNumber'] = self.Customer_PhoneNumber