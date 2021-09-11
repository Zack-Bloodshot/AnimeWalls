from telethon import events, Button
from Bot import bot, API_ID, API_HASH, BOT_TOKEN, CLIENT_ID, CLIENT_SECRET, USER_AGENT, logger, dandan
import asyncio
import asyncpraw
import requests
import os
from telethon.errors.rpcerrorlist import PhotoSaveFileInvalidError
import logging
import random

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
  if url[-3:] == ('jpg' or 'png'):
    file_name = f'{file_name}.{url[-3:]}'
  else:
    file_name = f'{file_name}.jpg'
  file = open(file_name, 'wb')
  file.write(r.content)
  file.close()
  return file_name

async def get_red_hash(name):
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
    hep = hep.replace(":", '')
    to_return = f'#{hep}'
    repa = ani.lower().replace('"', '')
    repa = repa.replace("/", '')
    repa = repa.replace(" ", '')
    repa = repa.replace('-', '')
    repa = repa.replace("'", '')
    repa = repa.replace(":", '')
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
  chars = characters.split(" ")
  count = 0
  text = ''
  if tscpy.lower() == 'original':
    return f'{chars} #og'
  for u in chars:
    try:
      u = u.replace('_', '')
      u = u.replace('-', '')
      u = u.replace('/', '')
      u = u.replace("'", '')
      u = u.replace("'", '')
      if not u == '':
        text += f'#{char[count].replace("_", "").split("(", 1)[0]}'
        text += ' '
      count += 1
    except IndexError:
      break 
  tscpy = tscpy.replace('_', '')
  tscpy = tscpy.replace('-', '')
  tscpy = tscpy.replace('/', '')
  tscpy = tscpy.split(' ', 1)[0]
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
    if not i.url != last_red:
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
    if post['large_file_url'] != last_dan:
      hashes = await get_dan_hash(post['tag_string_character'], post['tag_string_copyright'])
      last_dan = post['large_file_url']
      dl = down(post['large_file_url'], hashes)
      res = [dl, hashes, post['large_file_url']]
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
          mylog.info('Passed!, Didn\'t got info!')
        else:
            try:
              await bot.send_message(channel,hashes, file=path)
            except PhotoSaveFileInvalidError:
              try:
                await bot.send_message(channel, hashes, file=url)
              except Exception:
                print('Excepted!')
            await bot.send_message(channel,hashes, file=path, force_document=True)
            os.remove(path)
            mylog.info('Loop Success')
            mylog.info(f'Loop Info: Chose: {c}')
        await asyncio.sleep(20)    
        mylog.info("New Loop!")

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await bot.send_message(event.chat_id, "Is on ^_-")


loop.run_until_complete(send_wall())

bot.start()

bot.run_until_disconnected()
