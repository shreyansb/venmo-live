import redis
import json
import settings
import datetime
from time import sleep
from pymongo.connection import Connection

def main():
    r = redis.Redis()
    mongo_pointer = RemoteMongoConnect()
    last_datetime = datetime.datetime.now()
    # Grab latest timestamp, save, fetch all greater than latest, reset latest to last in list
    while True:
        spec = {
            "event_datetime":{ 
                "$gt": last_datetime 
            },
            "cat": {
                "$in": ["pay","charge","signup"]
            }
        }
        results = mongo_pointer.find(spec)
        result_datetimes = []
        for result in results:
            result_datetimes.append(result.get('event_datetime'))
	    del result['_id']
	    for k, v in result.iteritems():
	        if type(v) == datetime.datetime: del result[k]
            r.publish(settings.CHANNEL_NAME, json.dumps(result))
	if result_datetimes:
	    last_datetime = max(result_datetimes)
        sleep(1)

def RemoteMongoConnect():
    connection = Connection(settings.MONGO_HOST)
    db = connection[settings.MONGO_DB_NAME]
    return db[settings.MONGO_COLLECTION_NAME]


if __name__ == "__main__":
    main()
