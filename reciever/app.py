import connexion
from flask import jsonify,request
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import datetime
import requests
import logging
import logging.config
import uuid
import yaml
import datetime
import json
import requests


with open('reciever/app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())


with open('reciever/log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def report_order_status(body):
    
    trace_id = uuid.uuid4()  # Can use uuid, random, datetime
    body["trace_id"] = str(trace_id)

    mysql_endpoint = app_config['eventstore1']['url']
    headers = {"Content-Type": "application/json"}
    response = requests.post(mysql_endpoint, json=body, headers=headers)

    logger.info(f"Received event report_order_status request with a trace id of {trace_id}")
    logger.info(f"Returned event report_order_status response (Id: {trace_id}) with status {response.status_code}")
    return NoContent, 201

def reportETA(body):
    trace_id = uuid.uuid4()  # Can use uuid, random, datetime
    body["trace_id"] = str(trace_id)

    mysql_endpoint = app_config['eventstore2']['url']
    headers = {"Content-Type": "application/json"}
    response = requests.post(mysql_endpoint, json=body, headers=headers)

    logger.info(f"Received event reportETA request with a trace id of {trace_id}")
    logger.info(f"Returned event reportETA response (Id: {trace_id}) with status {response.status_code}")
    return NoContent, 201


app = connexion.FlaskApp(__name__,specification_dir='')
app.add_api("openapi.yml")



if __name__ == "__main__":
    app.run(port=8080)

