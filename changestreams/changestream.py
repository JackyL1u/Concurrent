from pymongo import MongoClient
from dotenv import load_dotenv
import os
from tools.redis_connection import master
import json

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URL"))
db = client['concurrent']

# Start a changestream
cursor = db["test-data"].watch(full_document='updateLookup')

while True:
    try:
        change = cursor.next()
        requireFetch = False
        if change.get("operationType") in ["insert", "update"]:
            requireFetch = True
        if requireFetch:
            users = db["test-data"].find({}, {"_id": False})
            master.set("users", json.dumps(list(users)))
    except StopIteration:  # recreate cursor is connection is closed
        cursor = db.mycollection.watch(full_document='updateLookup')
    except Exception as e:
        print(e, flush=True)
