from telethon import events, Button
from Bot import bot, API_ID, API_HASH, BOT_TOKEN, CLIENT_ID, CLIENT_SECRET, USER_AGENT, logger
import asyncio
import asyncpraw
import requests
import os

reddit = asyncpraw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, user_agent = USER_AGENT)

loop = asyncio.get_event_loop()

#@bot.on(events.NewMessage(pattern='sendonetime', incoming=True))
async def sendone(mikey):
  channel = await bot.get_entity(f't.me/AnimeWallsForU')
  text = 'The Walls here:\n\n\t\t#og'
  await bot.send_message(channel, text)
  #await bot.send_message(channel, text)

def down(url: str, hashes: str):
  r = requests.get(url)
  file_name = hashes.replace('#', '')
  file_name = file_name.replace(' ', '_')
  if url[-3:] == ('jpg' or 'png'):
    file_name = f'{file_name}.{url[-3:]}'
  else:
    file_name = f'{file_name}.jpg'
  file = open(file_name, 'wb')
  file.write(r.content)
  file.close()
  return file_name

async def get_hash(name):
  channel = await bot.get_entity(f't.me/AnimeWallsForU')
  hek = name.split('[', 1)
  ani = hek[1].split(']', 1)[0]
  if ani == 'Original':
    to_return = f'{hek[0]} #og'
    return to_return
  else:
    hep = hek[0].lower().replace('"', '')
    hep = hep.replace('/', '')
    hep = hep.replace(' ', '')
    hep = hep.replace('-', '')
    hep = hep.replace("'", '')
    to_return = f'#{hep}'
    repa = ani.lower().replace('"', '')
    repa = repa.replace("/", '')
    repa = repa.replace(" ", '')
    repa = repa.replace('-', '')
    repa = repa.replace("'", '')
    nime = f'#{repa}'
    to_return = to_return + ' ' + nime 
    get = await bot.get_messages(channel, ids=4)
    rtext = get.raw_text
    spl = get.raw_text.split('The Walls here:\n', 1)[1]
    spl2 = spl.split('\n')
    if nime not in spl:
      text = f'\n\t\t{nime}'
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
            print(i.url)
            if i.is_gallery:
              for u in i.media_metadata:
                dl = down(i.media_metadata[u]['s']['u'])
                await bot.send_message(channel,hashes, file=dl)
                await bot.send_message(channel,hashes, file=dl, force_document=True)
                os.remove(dl)
            else:
              dl = down(i.url, hashes)
              await bot.send_message(channel,hashes, file=dl)
              await bot.send_message(channel,hashes, file=dl, force_document=True)
              os.remove(dl)
            last = i.url
        await asyncio.sleep(60)    
        print("loop comp")

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await bot.send_message(event.chat_id, "Is on ^_-")


loop.run_until_complete(kang_reddit())

bot.start()

bot.run_until_disconnected()
