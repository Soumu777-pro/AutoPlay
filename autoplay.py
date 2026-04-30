import asyncio
import random
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL

from db import is_played, mark_played, get_autoplay
from music.youtube import random_query  # (optional helper)
from main import vc   # PyTgCalls instance (from main.py)


# ───────── AUTOPLAY STATE ─────────
autoplay_state = {}


# ───────── YOUTUBE FETCH ─────────
def fetch_song(query):
    ydl = YoutubeDL({"format": "bestaudio", "quiet": True})
    info = ydl.extract_info(f"ytsearch1:{query}", download=False)
    entry = info["entries"][0]

    return entry["url"], entry["title"]


# ───────── RANDOM SEED SYSTEM ─────────
SEEDS = [
    "trending songs 2026",
    "bollywood hits",
    "lofi music",
    "english top songs",
    "dj remix bass",
    "sad songs mix",
    "party songs",
]


def get_random_query():
    return random.choice(SEEDS)


# ───────── MAIN AUTOPLAY ENGINE ─────────
async def autoplay_loop(chat_id, vc_client):

    while autoplay_state.get(chat_id):

        try:
            query = get_random_query()

            # skip if already played
            if is_played(chat_id, query):
                continue

            url, title = fetch_song(query)

            mark_played(chat_id, query)

            print(f"🎧 Now Playing: {title}")

            await vc_client.join_group_call(
                chat_id,
                AudioPiped(url)
            )

            # approximate wait (can be improved later)
            await asyncio.sleep(180)

        except Exception as e:
            print(f"Error in autoplay: {e}")
            await asyncio.sleep(5)


# ───────── CONTROL FUNCTIONS ─────────
def start_autoplay(chat_id):
    autoplay_state[chat_id] = True


def stop_autoplay(chat_id):
    autoplay_state[chat_id] = False
