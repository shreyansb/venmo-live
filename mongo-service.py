import redis
import pymongo
import settings
from time import sleep
from pymongo.connection import Connection

def main():
    r = redis.Redis()
    mongo_pointer = RemoteMongoConnect()
    # Grab latest timestamp, save, fetch all greater than latest, reset latest to last in list
    while True:
        sleep(1)

def RemoteMongoConnect():
    connection = Connection(settings.MONGO_HOST)
    db = connection[settings.MONGO_DB_NAME]
    return db[settings.MONGO_COLLETION_NAME]




if __name__ == "__main__":
    main()
