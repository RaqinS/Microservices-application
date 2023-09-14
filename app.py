import connexion
from connexion import NoContent
import json



def report_order_status(body):
    json_str = json.dumps(body)
    with open('order_status.json','a') as fh:
        fh.write(json_str)


    return "order status has been reported"

def reportETA(body):
    json_str = json.dumps(body)
    with open('reportETA.json','a') as fh:
        fh.write(json_str)

    return "location information has been reported"

app = connexion.FlaskApp(__name__,specification_dir='')
app.add_api("openapi.yml")



if __name__ == "__main__":
    app.run(port=8080)

