import discord
import os
import requests
import json
import random
import urllib.request
from discord.ext import commands
from datetime import datetime

def composeURLPhotos(apiCall, photoType) :
  response = requests.get(apiCall)
  obj = json.loads(response.text)
  url_to_file = {}
  numOfPhotos = len(obj[photoType])
  if numOfPhotos == 0 :
    return None
  if numOfPhotos < 3 :
    for photos in obj[photoType] :
      url_to_file[photos['img_src']] = photos['img_src'].split("/")[-1:][0]
  else :
    for photos in random.sample(range(0, numOfPhotos), 3) :
      url = obj[photoType][photos]["img_src"]
      file_name = url.split("/")[-1:][0]
      rover = obj[photoType][photos]["rover"]["name"]
      camera = obj[photoType][photos]["camera"]["full_name"]
      date_taken = obj[photoType][photos]["earth_date"]

      url_to_file[url] = [file_name, rover, camera, date_taken]
  return url_to_file

def composeURLSpace(apiCall, photoType) :
  response = requests.get(apiCall)
  obj = json.loads(response.text)
  url_to_file = {}
  numOfPhotos = len(obj[photoType])
  if numOfPhotos == 0 :
    return None
  else:
    url = obj[photoType]
    file_name = url.split("/")[-1:][0]
    url_to_file[url] = file_name
  return url_to_file

client = commands.Bot(command_prefix = '~')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def MarsPOTD(ctx):
    url_to_file = composeURLPhotos('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key=DEMO_KEY', 'latest_photos')
    if url_to_file == None:
      await ctx.channel.send("No Photos Available")
    else:
      await ctx.channel.send('Here are Pictures of the Day for Mars!')
      for urls in url_to_file:
        file_name = url_to_file[urls][0]
        urllib.request.urlretrieve(urls, file_name)
        await ctx.channel.send('_ _')
        await ctx.channel.send('Rover ' + url_to_file[urls][1] + ' \|| ' + url_to_file[urls][2] + ' || ' + url_to_file[urls][3])
        await ctx.channel.send(file=discord.File(file_name))
        os.remove(file_name)


@client.command()
async def MarsDate(ctx, date):
  if bool(datetime.strptime(date, "%Y-%m-%d")) :
    url_to_file = composeURLPhotos("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key=4hvbdm3crmOBYueVE4FJSwRG3f1vhZykwNhgrqaW&earth_date={}".format(date), 'photos')
    if url_to_file == None :
     await ctx.channel.send("No Photos Available")
    else :
        await ctx.channel.send('Here are Mars Photos from '+date+'!')
        for urls in url_to_file :
          file_name = url_to_file[urls][0]
          urllib.request.urlretrieve(urls, file_name)
          await ctx.channel.send('_ _')
          await ctx.channel.send('Rover ' + url_to_file[urls][1] + ' \|| ' + url_to_file[urls][2] + ' || ' + url_to_file[urls][3])
          await ctx.channel.send(file=discord.File(file_name))
          os.remove(file_name)
   else :
     await ctx.channel.send('Please enter a valid date in the following format: YYYY-MM-DD')

@client.command()
async def MarsWeather(ctx):
  await ctx.channel.send('Fetching Weather Information from Mars from the Past 7 Sol (Martion Days)')
  

@client.command()
async def SpacePOTD(ctx):
  await ctx.channel.send('Heres the Picture of the Day!')
  url_to_file = composeURLSpace('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY', 'hdurl')
  for urls in url_to_file:
      file_name = url_to_file[urls]
      urllib.request.urlretrieve(urls, file_name)
      await ctx.channel.send(file=discord.File(file_name))
      os.remove(file_name)

@client.command()
async def SpaceDate(ctx, date):
  formt = "%Y-%m-%d"
  try:
    res = bool(datetime.strptime(date, formt))
  except ValueError:
    res = False
    await ctx.channel.send('Please enter a valid date in the following format: YYYY-MM-DD')
  if(res):
    apiURL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={}".format(date)
    url_to_file = composeURLSpace(apiURL, 'hdurl')
  if url_to_file == None:
      await ctx.channel.send("No Photos Available")
  else:
    msg = 'Here are some Beautiful Pictures of Space from '+date+'!'
    await ctx.channel.send(msg)
    for urls in url_to_file:
      file_name = url_to_file[urls]
      urllib.request.urlretrieve(urls, file_name)
      await ctx.channel.send(file=discord.File(file_name))
      os.remove(file_name) 

@client.command()
async def SpaceDateRange(ctx, date1, date2):
  formt = "%Y-%m-%d"
  try:
    res = bool(datetime.strptime(date1, formt))
    res2 = bool(datetime.strptime(date2, formt))
  except ValueError:
    res = False
    res2 = False
  if(res|res2):
    apiURL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&start_date={}&end_date={}".format(date1, date2)
    url_to_file = composeURLSpace(apiURL, 'hdurl')
    await ctx.channel.send('Please enter a valid date in the following format: YYYY-MM-DD')
  if url_to_file == None:
      await ctx.channel.send("No Photos Available")
  else:
    msg = 'Here are some Beautiful Pictures of Space from '+date1+' - '+date2+'!'
    await ctx.channel.send(msg)
    


client.run(os.getenv('TOKEN'))