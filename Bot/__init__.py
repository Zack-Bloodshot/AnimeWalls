from os import getenv
from dotenv import load_dotenv
from telethon import TelegramClient
import logging 
from pybooru import Danbooru

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")

load_dotenv()

API_ID= int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
USER_AGENT = getenv("USER_AGENT")
DANUSER = getenv('DANUSER')
DANAPI = getenv('DANAPI')

dandan = Danbooru('danbooru', username=DANUSER, api_key=DANAPI)

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)