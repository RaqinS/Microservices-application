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
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from flask_cors import CORS, cross_origin

# Load configuration from app_conf.yml
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f)

# Load logging configuration from log_conf.yml
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
logging.config.dictConfig(log_config)

# Create a logger
logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(
    f"mysql+pymysql://{app_config['datastore']['user']}:{app_config['datastore']['password']}@{app_config['datastore']['hostname']}:{app_config['datastore']['port']}/{app_config['datastore']['db']}"
)
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

logger.info("Connecting to DB. Hostname: {}:{}, Port: {}".format(app_config['datastore']['hostname'], app_config['datastore']['port'], app_config['datastore']['db']))

def report_order_status(body):
    """ Receives an order status update """

    session = DB_SESSION()

    order_status = Order_status(
        OrderID=body['OrderID'],
        CustomerAdress=body['CustomerAdress'],
        timestamp=body['timestamp'],
        OrderType=body['OrderType'],
        RestaurantID=body['RestaurantID'],
        Customer_PhoneNumber=body['Customer_PhoneNumber'],
        Tip=body['Tip'],
        trace_id=body['trace_id']
    )

    session.add(order_status)

    session.commit()
    session.close()

    logger.debug("Stored Order Status with OrderID %s and trace id %s" %
                 (body["OrderID"], body["trace_id"]))

    return NoContent, 201


def report_order_eta(body):
    """ Receives an order ETA update """

    session = DB_SESSION()

    order_eta = OrderETA(
        OrderID=body['OrderID'],
        CustomerLatitude=body['CustomerLatitude'],
        CustomerLongitude=body['CustomerLongitude'],
        RestaurantLatitude=body['RestaurantLatitude'],
        RestaurantLongitude=body['RestaurantLongitude'],
        DriverLatitude=body['DriverLatitude'],
        DriverLongitude=body['DriverLongitude'],
        OrderType=body['OrderType'],
        Distance=body['Distance'],
        timestamp=body['timestamp'],
        trace_id=body['trace_id']
    )

    session.add(order_eta)

    session.commit()
    session.close()

    logger.debug("Stored Order ETA for OrderID %s with trace id %s" %
                 (body["OrderID"], body["trace_id"]))

    return NoContent, 201



def get_order_status(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    
    readings = session.query(Order_status).filter(Order_status.date_created <=
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
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    readings = session.query(OrderETA).filter(OrderETA.date_created <=
                                                   timestamp_datetime)
    results_list = []

    for reading in readings:
        result = reading.to_dict()
        results_list.append(result)
            

    session.close()

    logger.info(f"Query for ETAs after {timestamp} returns {len(results_list)} results")

    return results_list, 200

def process_messages():
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    
    
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        
        if msg["type"] == "order_status":
            # Create an instance of the Order_status model
         
            report_order_status(payload)
           

        # Assuming you have a similar structure for OrderETA
        elif msg["type"] == "ETA":
            

            report_order_eta(payload)



        consumer.commit_offsets()
            
    



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)


