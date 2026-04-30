import asyncio
from pytgcalls.types.input_stream import AudioPiped
from music.youtube import fetch_song, random_query
from db import is_played, mark_played

autoplay_state = {}
current_stream = {}  # track VC session


async def autoplay_loop(chat_id, vc):

    while autoplay_state.get(chat_id):

        try:
            query = random_query()

            url, title = fetch_song(query)

            # skip repeats (title based)
            if is_played(chat_id, title):
                continue

            mark_played(chat_id, title)

            print(f"🎧 Playing: {title}")

            # ONLY join once (important fix)
            if chat_id not in current_stream:
                await vc.join_group_call(
                    chat_id,
                    AudioPiped(url)
                )
                current_stream[chat_id] = True
            else:
                await vc.change_stream(
                    chat_id,
                    AudioPiped(url)
                )

            # better fallback timing (can improve later)
            await asyncio.sleep(10)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(3)


def start_autoplay(chat_id):
    autoplay_state[chat_id] = True


def stop_autoplay(chat_id):
    autoplay_state[chat_id] = False
    current_stream.pop(chat_id, None)
