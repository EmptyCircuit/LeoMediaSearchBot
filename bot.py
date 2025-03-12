import os
import time
import logging
import logging.config

from pyromod import listen
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from utils import Media

# Load environment variables with fallback values
SESSION = os.getenv("SESSION", "my_bot")
APP_ID = int(os.getenv("APP_ID", "0"))  # Ensure it is an integer
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Ensure required variables are set
if APP_ID == 0 or not API_HASH or not BOT_TOKEN:
    raise ValueError("Missing required environment variables: APP_ID, API_HASH, or BOT_TOKEN")

# Configure logging
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)

# Time synchronization fix
def sync_time():
    try:
        import ntplib
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        os.environ['TZ'] = 'Asia/Kolkata'  # Change timezone if needed
        time.tzset()
        print("Time synced:", time.ctime(response.tx_time))
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
