from telethon import events, Button
from Bot import bot, API_ID, API_HASH, BOT_TOKEN, CLIENT_ID, CLIENT_SECRET, USER_AGENT, logger, dandan
import asyncio
import asyncpraw
import requests
import os
from telethon.errors.rpcerrorlist import PhotoSaveFileInvalidError
import logging
import random
import re

reddit = asyncpraw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, user_agent = USER_AGENT)

loop = asyncio.get_event_loop()

last_red = ''
last_dan = ''

mylog = logging.getLogger('animewalls')

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
  if url[-3:] in ('jpg', 'png'):
    file_name = f'{file_name[:20]}_@AnimeWallsForU.{url[-3:]}'
  else:
    file_name = f'{file_name[:20]}_@AnimeWallsForU.jpg'
  file = open(file_name, 'wb')
  file.write(r.content)
  file.close()
  return file_name

async def get_red_hash(name):
  channel = await bot.get_entity(f't.me/AnimeWallsForU')
  hek = name.split('[', 1)
  try:
    ani = hek[1].split(']', 1)[0]
  except IndexError:
    ani = '#nontag'
  if ani == 'Original':
    to_return = f'{hek[0]} #og'
    return to_return
  else:
    hep = re.sub(r'[^\W]+', '', hek[0].lower())
    to_return = f'#{hep}'
    repa = re.sub('[^\W]+', '', ani.lower())
    nime = f'#{repa}'
    to_return = to_return + ' ' + nime 
    get = await bot.get_messages(channel, ids=4)
    rtext = get.raw_text
    spl = get.raw_text.split('The Walls here:\n', 1)[1]
    if nime not in spl:
      text = f'\n\t\t{nime}'
      rtext += text 
      await get.edit(rtext)
    return to_return

async def get_dan_hash(characters, tscpy):
  channel = await bot.get_entity(f't.me/AnimeWallsForU')
  chars = characters.split(" ")
  count = 0
  text = ''
  if tscpy.lower() == 'original':
    return f'{characters} #og'
  for u in chars:
      try:
        u = u.split('(', )[0]
      except IndexError:
        u = u
      u = re.sub(r'[^\W]+', '', u.lower())
      if not u == '':
        text += f'#{u}'
        text += ' '
  tscpy = tscpy.split('(', 1)[0].lower()
  tscpy = tscpy.split(' ', 1)[0]
  tscpy = re.sub('[^\W]+', '', tscpy)
  tscpy = f'#{tscpy}'
  text+= tscpy
  get = await bot.get_messages(channel, ids=4)
  rtext = get.raw_text
  spl = get.raw_text.split('The Walls here:\n', 1)[1]
  #spl2 = spl.split('\n')
  if tscpy not in spl:
      text = f'\n\t\t{tscpy}'
      rtext += text 
      await get.edit(rtext)
  return text

async def kang_reddit():
  global last_red
  li = ['jpg', 'png']
  subred = await reddit.subreddit("Animewallpaper")
  new = subred.new(limit = 1)
  res = []
  async for i in new:
    if i.url != last_red:
      hashes = await get_red_hash(i.title)
      print(i.url)
      last_red = i.url 
      if i.url[-3:] not in li:
        print('passing...')
      else:
        dl = down(i.url, hashes)
        res = [dl, hashes, i.url]
  return res 
      
async def danparse():
  global last_dan
  rndpg = random.randint(1, 1000)
  posts = dandan.post_list(tags='rating:s', page=rndpg, limit=1)
  res = []
  for post in posts:
    try:
      if post['file_url'] != last_dan:
        hashes = await get_dan_hash(post['tag_string_character'], post['tag_string_copyright'])
        last_dan = post['file_url']
        dl = down(post['file_url'], hashes)
        res = [dl, hashes, post['file_url']]
    except KeyError:
      pass
  return res
    

async def send_wall():
    channel = await bot.get_entity(f"t.me/AnimeWallsForU")
    last = ''
    while True:
        sources = ['danbooru', 'reddit']
        c = random.choice(sources)
        if c == 'danbooru':
          result = await danparse()
        else:
          result = await kang_reddit()
        if len(result) < 3:
          mylog.info(f'Passed!, Didn\'t got info! Choice: {c}')
          mylog.info(f'Request: {result}')
        else:
            try:
              await bot.send_message(channel, result[1], file=result[0])
            except PhotoSaveFileInvalidError:
              try:
                await bot.send_message(channel, result[1], file=result[2])
              except Exception:
                print('Excepted!')
            await bot.send_message(channel, result[1], file=result[0], force_document=True)
            os.remove(result[0])
            mylog.info('Loop Success')
            mylog.info(f'Loop Info: Chose: {c}')
        await asyncio.sleep(60)    
        mylog.info("New Loop!")

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await bot.send_message(event.chat_id, "Is on ^_-")


loop.run_until_complete(send_wall())

bot.start()

bot.run_until_disconnected()
