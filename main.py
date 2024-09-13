# bot.py
import os
import discord
from pybase64 import standard_b64decode as DECODE
from discord.ext import commands
import requests
import random
# Decode base64 twice
TOKEN = str(DECODE(DECODE(
    b'VFZSSk5FMVVVVEpQVkVFeFRXcE5ORTVFUlRSTmFrazBUV2N1UjFaMFN6VkpMamhKUlZZNWFEaGhOWFJrVkdkSFpYbEpVMHA1VG5wT1VuQnVOMVpwYVhwSloyNTJlVVZ6')))[
        2:-1]
#client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def start(ctx):
    await ctx.send(f'{":stop_button:"*5}\n'*5)

@bot.command()
async def rickroll(ctx):
    os.system('"C:\Program Files\Google\Chrome\Application\chrome.exe" https://www.youtube.com/watch?v=xvFZjo5PgG0')

@bot.command()
async def lose(ctx):
    await ctx.send(get_random_gif_url())











def get_random_gif_url(limit=10):
    params = {
        'api_key': str(DECODE(DECODE(b'VTNKMFFqUTViMjh6TjA1Sk0zSndPVkZrUlVoWVVUVnpiRW8yVFVsM1oyWT0=')))[2:-1],
        'tag': '',
        "q":'explosion' ,
        'limit' : limit,# You can specify a tag to get GIFs related to that tag
        'rating': 'G'  # You can specify a rating like 'G', 'PG', etc.
    }

    response = requests.get('https://api.giphy.com/v1/gifs/search', params=params)

    if response.status_code == 200:
        data = response.json()
        gifs = data['data']

        if gifs:
            # Pick a random GIF from the list
            random_gif = random.choice(gifs)
            gif_url = random_gif['images']['original']['url']
            return gif_url
        else:
            print("No GIFs found for the query.")
            return None



bot.run(TOKEN)
