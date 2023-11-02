import connexion
from flask import jsonify,request
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from OrderETA import OrderETA
from Order_status import Order_status
import datetime
import requests
import logging
import logging.config
import uuid
import yaml
import datetime
import json
import requests

# Load configuration from app_conf.yml
with open('storage/app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f)

# Load logging configuration from log_conf.yml
with open('storage/log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
logging.config.dictConfig(log_config)

# Create a logger
logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(
    f"mysql+pymysql://{app_config['datastore']['user']}:{app_config['datastore']['password']}@{app_config['datastore']['hostname']}:{app_config['datastore']['port']}/{app_config['datastore']['db']}"
)
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def report_order_status(body):
    trace_id = uuid.uuid4()
    session = DB_SESSION()

    orders = Order_status(
        OrderID=body['OrderID'],
        CustomerAdress=body['CustomerAdress'],
        timestamp=body['timestamp'],
        RestaurantID=body['RestaurantID'],
        OrderType=body['OrderType'],
        Customer_PhoneNumber=body['Customer_PhoneNumber'],
        Tip=body['Tip'],
        trace_id=body['trace_id']
    )
    session.add(orders)

    session.commit()
    session.close()

    logger.debug(f"Received event report_order_status request with a trace id of {trace_id}")
    

    return NoContent, 201

def reportETA(body):
    trace_id = uuid.uuid4()
    session = DB_SESSION()

    ETA = OrderETA(
        OrderID=body['OrderID'],
        CustomerLatitude=body['CustomerLatitude'],
        CustomerLongitude=body['CustomerLongitude'],
        DriverLatitude=body['DriverLatitude'],
        DriverLongitude=body['DriverLongitude'],
        RestaurantLatitude=body['RestaurantLatitude'],
        RestaurantLongitude=body['RestaurantLongitude'],
        Distance=body['Distance'],
        OrderType=body['OrderType'],
        timestamp=body['timestamp'],
        trace_id=body['trace_id']
    )
    session.add(ETA)

    session.commit()


    session.close()

    logger.debug(f"Received event report_order_status request with a trace id of {trace_id}")

    return NoContent, 201

def get_order_status(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
    
    readings = session.query(Order_status).filter(Order_status.date_created >=
                                                   timestamp_datetime)
    
    results_list = []
    
    for reading in readings:
        result = reading.to_dict()
        results_list.append(result)
        logger.debug("Retrieved: %s" % result)

    logger.info(f"Query for orders after {timestamp} returns {len(results_list)} results")
    
    return results_list, 200


def get_order_ETA(timestamp):

    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")

    readings = session.query(OrderETA).filter(OrderETA.date_created >=
                                                   timestamp_datetime)
    results_list = []

    for reading in readings:
        result = reading.to_dict()
        results_list.append(result)
        logger.debug("Retrieved: %s" % result)

    session.close()

    logger.info(f"Query for ETAs after {timestamp} returns {len(results_list)} results")

    return results_list, 200



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)


