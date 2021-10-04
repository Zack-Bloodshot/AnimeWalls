from telethon import events, Button
from Bot import bot, API_ID, API_HASH, BOT_TOKEN, CLIENT_ID, CLIENT_SECRET, USER_AGENT, logger, dandan, check_exist, add_url
import asyncio
import asyncpraw
import requests
import os
from telethon.errors.rpcerrorlist import PhotoSaveFileInvalidError, ImageProcessFailedError
import logging
import random
import re
from anime_list import the_list


reddit = asyncpraw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, user_agent = USER_AGENT)

loop = asyncio.get_event_loop()

last_red = ''
last_dan = ''

mylog = logging.getLogger('Animewalls')

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
  #channel = await bot.get_entity(f't.me/AnimeWallsForU')
  hek = name.split('[', 1)
  try:
    ani = hek[1].split(']', 1)[0]
  except IndexError:
    ani = '#nontag'
  if ani == 'Original':
    to_return = f'{hek[0]} #og'
    return to_return
  else:
    hep = re.sub('[\W_]+', '', hek[0].lower())
    to_return = f'#{hep}'
    repa = re.sub('[\W_]+', '', ani.lower())
    nime = f'#{repa}'
    to_return = to_return + ' ' + nime 
    #get = await bot.get_messages(channel, ids=4)
    #rtext = get.raw_text
    #spl = get.raw_text.split('The Walls here:\n', 1)[1]
    #if nime not in spl:
      #text = f'\n\t\t{nime}'
      #rtext += text 
      #await get.edit(rtext)
    return to_return

async def get_dan_hash(characters, tscpy):
  #channel = await bot.get_entity(f't.me/AnimeWallsForU')
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
      u = re.sub('[\W_]+', '', u.lower())
      if not u == '':
        text += f'#{u}'
        text += ' '
  tscpy = tscpy.split('(', 1)[0].lower()
  tscpy = tscpy.split(' ', 1)[0]
  tscpy = re.sub('[\W_]+', '', tscpy)
  tscpy = f'#{tscpy}'
  text+= tscpy
  #get = await bot.get_messages(channel, ids=4)
  #rtext = get.raw_text
  #spl = get.raw_text.split('The Walls here:\n', 1)[1]
  #spl2 = spl.split('\n')
  #if tscpy not in spl:
  #    text = f'\n\t\t{tscpy}'
  #    rtext += text 
  #    await get.edit(rtext)
  return text

async def kang_reddit():
  global last_red
  subred = await reddit.subreddit("Animewallpaper")
  new = subred.new(limit = 1)
  res = []
  async for i in new:
    if check_exist(i.url):
      hashes = await get_red_hash(i.title)
      print(i.url)
      mylog.debug(f'Reddit-catch : {i.url}')
      add_url(i.url, 'reddit') 
      if i.url[-3:] in ('jpg', 'png'):
        dl = down(i.url, hashes)
        res = [dl, hashes, i.url]
        mylog.debug(f'Reddit-res: {res}')
        return res
      else:
        mylog.info(f'Twas Gallery: {i.url}')
  return res 
      
async def danparse():
  try:
    global last_dan
    rndpg = random.randint(1, 1000)
    tag_choices = ['rating:safe', 'scenery', 'no_humans' , 'building', 'tree',  'cloud', 'power_lines', 'nature', 'forest', 'sky', f'{random.choice(the_list)}']
    tag = random.choice(tag_choices)
    posts = dandan.post_list(tags=tag, page=rndpg, limit=1)
    res = []
    for post in posts:
      try:
        fu = post['file_url']
        if check_exist(fu):
          hashes = await get_dan_hash(post['tag_string_character'], post['tag_string_copyright'])
          add_url(fu, 'danbooru')
          dl = down(fu, hashes)
          res = [dl, hashes, fu]
      except KeyError:
        pass
    return res
  except Exception as e:
    mylog.error(e)
    

async def send_wall():
    channel = await bot.get_entity(f"t.me/AnimeWallForU")
    last = ''
    while True:
        sources = ['danbooru', 'reddit']
        c = random.choice(sources)
        if c == 'danbooru':
          result = await danparse()
        else:
          result = await kang_reddit()
        mylog.info(f'Request: {result}')
        try:
          if len(result) < 3:
            mylog.info(f'Passed!, Didn\'t got info! Choice: {c}')
          else:
              try:
                await bot.send_message(channel, result[1], file=result[0])
              except PhotoSaveFileInvalidError:
                try:
                  await bot.send_message(channel, result[1], file=result[2])
                except Exception:
                  print('Excepted!')
              except ImageProcessFailedError:
                try:
                  await bot.send_message(channel, result[1], file=result[2])
                except Exception:
                  print('Excepted!')
              await bot.send_message(channel, result[1], file=result[0], force_document=True)
              os.remove(result[0])
              mylog.info('Loop Success')
              mylog.info(f'Loop Info: Chose: {c}')
        except Exception as e:
          mylog.info(f'Loop failed: {e}')
        await asyncio.sleep(60)    
        mylog.info("New Loop!")

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await bot.send_message(event.chat_id, "Is on ^_-")


loop.run_until_complete(send_wall())

bot.start()

bot.run_until_disconnected()
