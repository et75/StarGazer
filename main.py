import discord
import os
import requests
import json
from PIL import Image
import urllib.request

#  img = Image.open(file_name)

#  img.show()




client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('~POTD'):
        await message.channel.send('Heres the Picture of the Day!')
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
        obj = json.loads(response.text)
        url = obj['hdurl']
        expl = obj['explanation']
        file_name = url.split("/")[-1:][0]
        print(file_name)
        urllib.request.urlretrieve(url, file_name)
        await message.channel.send(file=discord.File(file_name))
        await message.channel.send(expl)
        os.remove(file_name)

  if message.content.startswith('~MARS'):
        await message.channel.send('Heres the Picture of the Day!')
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
        obj = json.loads(response.text)
        count = 0
        for p in obj['latest_photos']:
          count = count + 1
          if count < 3:
            url = p['img_src']
            file_name = url.split("/")[-1:][0]
        print(file_name)
        urllib.request.urlretrieve(url, file_name)
        await message.channel.send(file=discord.File(file_name))
        os.remove(file_name)
        

client.run(os.getenv('TOKEN'))



'''
~POTD
  - default to today
~POTD YYYY-MM-DD
~Random #
~MarsPOTD
  - Latest Date
~MarsPOTD YYYY-MM-DD
~
'''