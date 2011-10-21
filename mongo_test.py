import redis
import venmo_live_settings
from time import sleep

def main():
    r = redis.Redis()
    # Grab latest timestamp, save, fetch all greater than latest, reset latest to last in list
    while True:
        r.publish(venmo_live_settings.CHANNEL_NAME, '{"from_username": "shreyans", "to_username": "julian", "to_user_img_url": "https://venmopics.appspot.com/u/v1/s/d0d7e184-141b-47f8-a05e-6c60b9fed65a", "locLat": null, "note": "for an epic soccer game", "amount": 1.01, "user": "shreyans", "locLong": null, "ip_address": "184.74.224.170", "from_user_img_url": "https://venmopics.appspot.com/u/v21/f/01fcf991-3592-4e40-bc8b-df3eb0c1f027"}')
        sleep(1)
    """
    {"from_username": "shreyans", "to_username": "julian", "to_user_img_url": "https://venmopics.appspot.com/u/v1/s/d0d7e184-141b-47f8-a05e-6c60b9fed65a", "locLat": null, "note": "for an epic soccer game", "amount": 1.01, "user": "shreyans", "locLong": null, "ip_address": "184.74.224.170", "from_user_img_url": "https://venmopics.appspot.com/u/v21/f/01fcf991-3592-4e40-bc8b-df3eb0c1f027"}

    {"signup_ip_address": null, "profile_picture": null, "user": "john-nylen"}

    {"from_username": null, "to_username": null, "to_user_img_url": null, "locLat": null, "note": null, "amount": 53.0, "user": "jeremiah-robison", "locLong": null, "ip_address": null, "from_user_img_url": null}

    {"from_username": null, "to_username": null, "to_user_img_url": null, "locLat": null, "note": null, "amount": 1000.0, "user": "skyfarm-expenses", "locLong": null, "ip_address": null, "from_user_img_url": null}

    {"signup_ip_address": null, "profile_picture": null, "user": "sun-jiujiu"}
    """



if __name__ == "__main__":
    main()
