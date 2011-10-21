import redis
import json
import venmo_live_settings
import datetime
from time import sleep
from pymongo.connection import Connection

def main():
    r = redis.Redis()
    mongo_pointer = RemoteMongoConnect()
    last_datetime = datetime.datetime.now()

    payment_keys = ['cat', 'user', 'ip_address', 'locLat', 'locLong', 
                    'amount', 'note', 
                    'to_username', 'from_username',
                    'to_user_img_url', 'from_user_img_url']
    signup_keys = ['cat', 'user', 'signup_ipaddress', 'profile_picture',
                   'locLat', 'locLong']
    required_keys = ['locLat', 'locLong']

    # Grab latest timestamp, save, fetch all greater than latest, reset latest to last in list
    while True:
        spec = {
            "event_datetime":{ 
                "$gt": last_datetime 
            },
            "cat": {
                "$in": ["pay","charge","signup_detailed"]
            }
        }
        results = mongo_pointer.find(spec)
        result_datetimes = []
        for result in results:
            result_datetimes.append(result.get('event_datetime'))
            result_dict = {}
            if result.get('cat') in ['pay', 'charge']:
                for k in payment_keys:
                    result_dict[k] = result.get(k)
            else:
                for k in signup_keys:
                    result_dict[k] = result.get(k)
            do_publish = True
            for k in required_keys:
                if not result_dict.get(k):
                    do_publish = False
                    break
            if do_publish:
                r.publish(venmo_live_settings.CHANNEL_NAME, json.dumps(result_dict))
	if result_datetimes:
	    last_datetime = max(result_datetimes)
        sleep(1)

def RemoteMongoConnect():
    connection = Connection(venmo_live_settings.MONGO_HOST)
    db = connection[venmo_live_settings.MONGO_DB_NAME]
    return db[venmo_live_settings.MONGO_COLLECTION_NAME]


if __name__ == "__main__":
    main()
