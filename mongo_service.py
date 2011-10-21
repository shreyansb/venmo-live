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

    events_to_find = ['pay', 'charge', 'signup_detailed']
    payment_keys = ['user', 'ip_address', 'locLat', 'locLong', 
                    'amount', 'note', 
                    'to_username', 'from_username',
                    'to_user_img_url', 'from_user_img_url']
    signup_keys = ['user', 'signup_ipaddress', 'profile_picture',
                   'locLat', 'locLong']
    comment_keys = ['user', 'signup_ipaddress', 'profile_picture',
                   'locLat', 'locLong']
    required_keys = ['locLat', 'locLong']

    # Grab latest timestamp, save, fetch all greater than latest, reset latest to last in list
    while True:
        spec = {
            "event_datetime":{ 
                "$gt": last_datetime 
            },
            "cat": {
                "$in": events_to_find
            }
        }
        results = mongo_pointer.find(spec)
        result_datetimes = []
        for result in results:
            result_datetimes.append(result.get('event_datetime'))
            category = result.get('cat')
            result_dict = {'cat':category}
            if category in ['pay', 'charge']:
                keys_to_add = payment_keys
            elif category == 'comment':
                keys_to_add = comment_keys
            else:
                keys_to_add = signup_keys
            for k in keys_to_add:
                result_dict[k] = result.get(k)
            do_publish = True
            for k in required_keys:
                if not result_dict.get(k):
                    do_publish = False
                    break
            if do_publish:
		print result_dict
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
