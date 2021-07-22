import discord
import os
import requests
import json
from PIL import Image
import urllib.request


response = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")

obj = json.loads(response.text)


url = obj['hdurl']
file_name = url.split("/")[-1:][0]

print(file_name)

urllib.request.urlretrieve(url, file_name)



img = Image.open(file_name)

img.show()

os.remove(file_name)

''''
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('~hello'):
        await message.channel.send('Hello!')

client.run(os.getenv('TOKEN'))
'''