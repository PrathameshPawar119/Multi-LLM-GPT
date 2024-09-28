import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

def dbconnect():
    client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
    return client["chat_app"]