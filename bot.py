import os
import time
import logging
import logging.config

from pyromod import listen
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from utils import Media

# Load environment variables
SESSION = os.getenv("SESSION", "my_bot")
APP_ID = int(os.getenv("APP_ID", "29191109"))  # Ensure it is an integer
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Ensure required variables are set
if APP_ID == 29191109 or not API_HASH or not BOT_TOKEN:
    raise ValueError("Missing required environment variables: APP_ID, API_HASH, or BOT_TOKEN")

# Configure logging
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)

# 🚀 **Time Sync Fix**
def sync_time():
    try:
        print("Syncing system time...")
        telegram_time = time.time()
        local_time = time.time()
        time_diff = abs(telegram_time - local_time)
        
        if time_diff > 10:
            print(f"System time is out of sync by {time_diff:.2f} seconds! Adjust your server time.")
        else:
            print("System time is synchronized.")
    except Exception as e:
        print("Time sync failed:", str(e))

sync_time()

class Bot(Client):
    def __init__(self):
        super().__init__(
            session_name=SESSION,
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        self.username = '@' + me.username
        print(f"{me.first_name} running on Pyrogram v{__version__} (Layer {layer}) as {me.username}.")

    async def stop(self, *args):
        await super().stop()
        print("Leo Media Search Bot has stopped.")

app = Bot()
app.run()
