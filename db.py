from pymongo import MongoClient
from config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# collections
played = db["played_songs"]
settings = db["settings"]
queue = db["queue"]
