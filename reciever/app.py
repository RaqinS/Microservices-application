import connexion
from flask import jsonify, request
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import datetime
import requests
import logging
import logging.config
import uuid
import yaml
import json
from pykafka import KafkaClient

with open('reciever/app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('reciever/log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def report_order_status(body):
    trace_id = uuid.uuid4() 
    body["trace_id"] = str(trace_id)

    # Kafka Producer setup
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

    msg = {
        "type": "order_status",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f"Received event report_order_status request with a trace id of {trace_id}")
    return NoContent, 201

def reportETA(body):
    trace_id = uuid.uuid4()
    body["trace_id"] = str(trace_id)

    # Kafka Producer setup
    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

    msg = {
        "type": "ETA",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f"Received event reportETA request with a trace id of {trace_id}")
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml")

if __name__ == "__main__":
    app.run(port=8080)
