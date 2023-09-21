import connexion
from connexion import NoContent
import json
from datetime import datetime



EVENT_FILE = 'events.json'
def logging(body, event_type):
    event = {
        "received_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "request_data": json.dumps(body)
    }
    json_str = json.dumps(event)

    
    requests = []
    try:
        with open(EVENT_FILE, 'r') as fh:
            requests = fh.readlines()
    except FileNotFoundError:
        pass


    requests.insert(0, json_str + '\n')

  
    requests = requests[:10]

    try:
        with open(EVENT_FILE, 'w') as fh:
            fh.writelines(requests)
            return f"{event_type} has been reported"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

def report_order_status(body):
    return logging(body, "order status")

def reportETA(body):
    return logging(body, "location information")


app = connexion.FlaskApp(__name__,specification_dir='')
app.add_api("openapi.yml")



if __name__ == "__main__":
    app.run(port=8080)

