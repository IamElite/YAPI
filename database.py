from pymongo import MongoClient
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client['bad_yt_api']
audio_ids = db['audio_ids']

def insert_audio_id(audio_id: str):
    """Insert audio ID with timestamp into MongoDB."""
    audio_ids.insert_one({"audio_id": audio_id, "date": datetime.datetime.utcnow()})

def get_stats():
    """Retrieve statistics for the home page."""
    return {
        'total_plays_requests': audio_ids.count_documents({}),
        'today_plays': audio_ids.count_documents({
            'date': {'$gte': datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)}
        }),
        'active_keys': 1
    }
