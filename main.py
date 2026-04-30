import asyncio
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

from config import API_ID, API_HASH, STRING_SESSION
from music.autoplay import autoplay_loop, autoplay_state

# ───────── CLIENT ─────────
app = Client(
    "vc-userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

# PyTgCalls VC engine
vc = PyTgCalls(app)

# ───────── START AUTOPLAY COMMAND ─────────
@app.on_message(filters.command("autoplay"))
async def autoplay_cmd(_, msg):

    chat_id = msg.chat.id

    if len(msg.command) < 2:
        return await msg.reply("Use: /autoplay on or off")

    mode = msg.command[1].lower()

    if mode == "on":
        autoplay_state[chat_id] = True
        await msg.reply("🎧 Autoplay Started (VC Music ON)")

        # start loop
        asyncio.create_task(autoplay_loop(chat_id, vc))

    elif mode == "off":
        autoplay_state[chat_id] = False
        await msg.reply("⛔ Autoplay Stopped")

# ───────── START BOT ─────────
async def main():
    await app.start()
    await vc.start()

    print("🔥 VC Music Userbot Running...")
    await idle()

    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
