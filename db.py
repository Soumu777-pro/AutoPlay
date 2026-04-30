from pymongo import MongoClient
from config import MONGO_URL, DB_NAME

# ───────── DATABASE CONNECTION ─────────
client = MongoClient(MONGO_URL)
db = client[DB_NAME]

played = db["played_songs"]
settings = db["settings"]
queue = db["queue"]

# ───────── SONG MEMORY (NO REPEAT SYSTEM) ─────────

def is_played(chat_id, song):
    """Check if song already played in this chat"""
    return played.find_one({
        "chat_id": chat_id,
        "song": song
    }) is not None


def mark_played(chat_id, song):
    """Mark song as played"""
    played.insert_one({
        "chat_id": chat_id,
        "song": song
    })


# ───────── AUTOPLAY STATE ─────────

def set_autoplay(chat_id, state: bool):
    """Enable/Disable autoplay per group"""
    settings.update_one(
        {"chat_id": chat_id},
        {"$set": {"autoplay": state}},
        upsert=True
    )


def get_autoplay(chat_id):
    """Get autoplay status"""
    data = settings.find_one({"chat_id": chat_id})
    return data["autoplay"] if data else False


# ───────── QUEUE SYSTEM ─────────

def add_to_queue(chat_id, song, url):
    """Add song to queue"""
    queue.insert_one({
        "chat_id": chat_id,
        "song": song,
        "url": url
    })


def get_next_song(chat_id):
    """Get next song from queue"""
    return queue.find_one({"chat_id": chat_id})


def clear_queue(chat_id):
    """Clear queue for a chat"""
    queue.delete_many({"chat_id": chat_id})
