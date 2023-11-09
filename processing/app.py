import connexion
from connexion import NoContent
import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
import json
import requests
import logging.config
import yaml

# External Application Configuration
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def get_stats():
    """ Gets processing stats """

    if os.path.isfile(app_config["datastore"]["filename"]):
        fh = open(app_config["datastore"]["filename"])
        full_stats = json.load(fh)
        fh.close()

        stats = {}
        if "furthest_distance" in full_stats:
            stats["furthest_distance"] = full_stats.get("furthest_distance", 0)
        if "highest_tip" in full_stats:   
            stats["highest_tip"] = full_stats.get("highest_tip", 0)
        if "num_orders" in full_stats:
            stats["num_orders"] = full_stats.get("num_orders", 0)
        if "num_customers" in full_stats:
            stats["num_customers"] = full_stats.get("num_customers", 0)

        logger.info("Found valid stats")
        logger.debug(stats)

        return stats, 200

    return NoContent, 404


def populate_stats():
    """ Periodically update stats """
    logger.info("Start Periodic Processing")

    stats = get_latest_processing_stats()

    last_updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if "last_updated" in stats.keys():
        last_updated = stats["last_updated"]

    # Processing orders based on the /order/status endpoint
    response = requests.get(app_config["eventstore"]["url"] + "/order/status?timestamp=" + last_updated)

    if response.status_code == 200:
        if "num_orders" in stats.keys():   
            stats["num_orders"] += len(response.json())
        else:
            stats["num_orders"] = len(response.json())

        if "num_customers" in stats.keys():   
            stats["num_customers"] += len(response.json())
        else:
            stats["num_customers"] = len(response.json())

        for event in response.json():
            if "highest_tip"  in stats.keys() and \
                event["Tip"] > stats.get("highest_tip", 0):
                stats["highest_tip"] = event["Tip"]
            elif "highest_tip" not in stats.keys():
                stats["highest_tip"] = event["Tip"]

            
            logger.debug("Processed Order event with id of %s" % event["OrderID"])

       
        logger.info("Processed %d Order_status readings" % len(response.json()))
    
    response = requests.get(app_config["eventstore"]["url"] + "/order/orderETA?timestamp=" + last_updated)

    if response.status_code == 200:
        for event in response.json():
            if "furthest_distance" in stats.keys() and \
                event["Distance"] > stats.get("furthest_distance", 0):
                stats["furthest_distance"] = event["Distance"]
            elif "furthest_distance" not in stats.keys():
                stats['furthest_distance'] = event["Distance"]

            logger.debug("Processed ETA event with id of %s" % event["trace_id"])

        logger.debug("Processed ETA event with id of %s" % event["trace_id"])
    stats["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 

    write_processing_stats(stats)

    logger.info("Done Periodic Processing")
    

def get_latest_processing_stats():
    """ Gets the latest stats object, or None if there isn't one """
    if os.path.isfile(app_config["datastore"]["filename"]):
        fh = open(app_config["datastore"]["filename"])
        full_stats = json.load(fh)
        fh.close()
        return full_stats

    return {
        "furthest_distance": 0,
        "highest_tip": 0,
        "num_orders": 0,
        "num_customers": 0,
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }


def write_processing_stats(stats):
    """ Writes a new stats object """
    fh = open(app_config["datastore"]["filename"], "w")
    fh.write(json.dumps(stats))
    fh.close()


def init_scheduler():
    """ Initializes the periodic background processing """
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)
