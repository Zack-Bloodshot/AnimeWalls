import logging 
from telethon import events, Button
from Bot import bot, API_ID, API_HASH, BOT_TOKEN, CLIENT_ID, CLIENT_SECRET, USER_AGENT
import asyncio
import asyncpraw

reddit = asyncpraw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, user_agent = USER_AGENT)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")

loop = asyncio.get_event_loop()

@bot.on(events.NewMessage(pattern='sendonetime', incoming=True))
async def sendone(mikey):
  channel = await bot.get_entity(f't.me/AnimeWallsForU')
  text = 'The Walls here: '
  await bot.send_message(channel, text)
  #await bot.send_message(channel, text)

async def get_hash(name):
  channel = await bot.get_entity(f't.me/AnimeWallsForU')
  hek = name.split('[', 1)
  ani = hek[1].split(']', 1)[0]
  if ani == 'Original':
    to_return = f'{hek[0]} #og'
    has = '#og'
    get = await bot.get_messages(channel, ids=3)
    rtext = get.raw_text
    spl = get.raw_text.split('The Walls here:\n', 1)[1]
    spl2 = spl.split('\n')
    if has not in spl:
      text = f'\n{has}'
      rtext += text 
      await get.edit(rtext)
    return to_return
  else:
    to_return = f'#{hek[0].lower().replace(" ", "")}'
    nime = f'#{ani.lower().replace(" ", "")}'
    to_return += nime 
    get = await bot.get_messages(channel, ids=2)
    rtext = get.raw_text
    spl = get.raw_text.split('The Walls here:\n', 1)[1]
    spl2 = spl.split('\n')
    if nime not in spl:
      text = f'\n{nime}'
      rtext += text 
      await get.edit(rtext)
    return to_return


async def kang_reddit():
    channel = await bot.get_entity(f"t.me/AnimeWallsForU")
    last = ''
    while True:
        subred = await reddit.subreddit("Animewallpaper")
        new = subred.new(limit = 1)
        async for i in new:
          if i.url != last:
            hashes = await get_hash(i.title)
            await bot.send_message(file=i.url, caption=hashes)
            await bot.send_message(file=i.url, caption=hashes, force_document=True)
        await asyncio.sleep(60)    
        print("nothing")

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await bot.send_message(event.chat_id, "Is on ^_-")


loop.run_until_complete(kang_reddit())

bot.run_until_disconnected()
