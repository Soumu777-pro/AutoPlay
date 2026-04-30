import asyncio
from pytgcalls.types.input_stream import AudioPiped

from music.youtube import fetch_song, random_query
from db import is_played, mark_played

autoplay_state = {}
current_chat = {}


# ───────── MAIN LOOP ─────────
async def autoplay_loop(chat_id, vc):

    while autoplay_state.get(chat_id):

        try:
            query = random_query()
            url, title = fetch_song(query)

            # no repeat (URL-based safe)
            if is_played(chat_id, url):
                await asyncio.sleep(2)
                continue

            mark_played(chat_id, url)

            print(f"🎧 Now Playing: {title}")

            # first time join
            if chat_id not in current_chat:
                try:
                    await vc.join_group_call(
                        chat_id,
                        AudioPiped(url)
                    )
                    current_chat[chat_id] = True

                except Exception as vc_err:
                    print("VC Join Error:", vc_err)
                    await asyncio.sleep(5)
                    continue

            else:
                try:
                    await vc.change_stream(
                        chat_id,
                        AudioPiped(url)
                    )

                except Exception as vc_err:
                    print("Stream Error, rejoining VC:", vc_err)
                    current_chat.pop(chat_id, None)
                    continue

            # realistic fallback delay
            await asyncio.sleep(180)

        except Exception as e:
            print("Autoplay Error:", e)
            await asyncio.sleep(5)


# ───────── CONTROLS ─────────
def start_autoplay(chat_id):
    autoplay_state[chat_id] = True


def stop_autoplay(chat_id):
    autoplay_state[chat_id] = False
    current_chat.pop(chat_id, None)
