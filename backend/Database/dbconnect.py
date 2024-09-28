import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

def get_database():
    # Connect to MongoDB
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    return client["chat_app"]