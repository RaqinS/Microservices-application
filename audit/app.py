from pykafka import KafkaClient
from pykafka.common import OffsetType
from flask import Flask, jsonify, request
import json
import logging
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("audit-service")

app = Flask(__name__)

# Load configuration from a file or environment variables
app_config = {
    "events": {
        "hostname": "your_vm_hostname",
        "port": 9092,
        "topic": "events"
    }
}

def get_kafka_client():
    return KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")

def process_messages():
    """ Process event messages """
    client = get_kafka_client()
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)

    for msg in consumer:
        if msg is not None:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            logger.info(f"Message: {msg}")
            # Process message
            # ...

@app.route('/blood_pressure', methods=['GET'])
def get_blood_pressure_reading():
    index = request.args.get('index', default=0, type=int)
    client = get_kafka_client()
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    logger.info(f"Retrieving BP at index {index}")
    
    try:
        for i, msg in enumerate(consumer):
            if i == index:
                msg_str = msg.value.decode('utf-8')
                msg = json.loads(msg_str)
                # Assuming msg is a dict with the correct structure
                return jsonify(msg), 200
    except Exception as e:
        logger.error(f"No more messages found - {str(e)}")
        logger.error(f"Could not find BP at index {index}")
        return jsonify({"message": "Not Found"}), 404

@app.route('/heart_rate', methods=['GET'])
def get_heart_rate_reading():
    index = request.args.get('index', default=0, type=int)
    client = get_kafka_client()
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    logger.info(f"Retrieving HR at index {index}")
    
    try:
        for i, msg in enumerate(consumer):
            if i == index:
                msg_str = msg.value.decode('utf-8')
                msg = json.loads(msg_str)
                # Assuming msg is a dict with the correct structure
                return jsonify(msg), 200
    except Exception as e:
        logger.error(f"No more messages found - {str(e)}")
        logger.error(f"Could not find HR at index {index}")
        return jsonify({"message": "Not Found"}), 404

if __name__ == '__main__':
    # Start the Flask app
    app.run(host="0.0.0.0", port=8080)
