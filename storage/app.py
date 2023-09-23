import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from OrderETA import OrderETA
from Order_status import Order_status
import datetime
import requests

DB_ENGINE = create_engine("sqlite:///readings.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def report_order_status(body):
    session = DB_SESSION()

    orders = Order_status(body['OrderID'],
                       body['CustomerAdress'],
                       body['TimeStamp'],
                       body['RestaurantID'],
                       body['OrderType'],
                       body['Customer_PhoneNumber']
    )
    session.add(orders)

    session.commit()

    mysql_endpoint = "http://localhost:8080"
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(mysql_endpoint, json=body, headers=headers)

    
    session.close()
    

    return NoContent, 201
def reportETA(body):

    session = DB_SESSION()

    ETA= OrderETA(body['OrderID'],
                       body['CustomerLatitude'],
                       body['CustomerLongitude'],
                       body['DriverLatitude'],
                       body['DriverLongitude'],
                       body['RestaurantLatitude'],
                       body['RestaurantLongitude'],
                       body['Distance'],
                       body['OrderType']
    )
    session.add(ETA)

    session.commit()

    mysql_endpoint = "http://localhost:8080"
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(mysql_endpoint, json=body, headers=headers)

    session.close()
    

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)


