import asyncio
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls

from config import API_ID, API_HASH, STRING_SESSION
from music.autoplay import (
    autoplay_loop,
    autoplay_state,
    start_autoplay,
    stop_autoplay
)

# ───────── CLIENT ─────────
app = Client(
    "vc-music-userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

# ───────── VC ENGINE ─────────
vc = PyTgCalls(app)

# track running tasks
tasks = {}


# ───────── AUTOPLAY COMMAND ─────────
@app.on_message(filters.command("autoplay") & filters.group)
async def autoplay_cmd(_, msg):

    chat_id = msg.chat.id

    if len(msg.command) < 2:
        return await msg.reply("Use: /autoplay on or off")

    mode = msg.command[1].lower()

    # ON
    if mode == "on":

        if autoplay_state.get(chat_id):
            return await msg.reply("⚠️ Already running")

        start_autoplay(chat_id)

        await msg.reply("🎧 Autoplay Started")

        # prevent duplicate tasks
        task = asyncio.create_task(autoplay_loop(chat_id, vc))
        tasks[chat_id] = task

    # OFF
    elif mode == "off":

        stop_autoplay(chat_id)

        # cancel running task
        task = tasks.get(chat_id)
        if task:
            task.cancel()

        await msg.reply("⛔ Autoplay Stopped")


# ───────── START BOT ─────────
async def main():
    await app.start()
    await vc.start()

    print("🔥 VC Music Userbot Running...")

    await idle()

    await app.stop()
    await vc.stop()


if __name__ == "__main__":
    asyncio.run(main())
