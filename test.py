# bot.py
import os
import discord
from pybase64 import standard_b64decode as DECODE
from discord.ext import commands
from laddawan import *
import requests
import random

current_board = None
current_revealed = None
size = None
bombs = None

LEVELS = {
    'easy': {'size': 5, 'bombs': 3},
    'medium': {'size': 7, 'bombs': 12},
    'hard': {'size': 10, 'bombs': 30},
    'impossible': {'size': 15, 'bombs': 99}
}

PREFIX = "$"
e_0 = ":blue_square:"
e_1 = ":one:"
e_2 = ":two:"
e_3 = ":three:"
e_4 = ":four:"
e_5 = ":five:"
e_6 = ":six:"
e_7 = ":seven:"
e_8 = "<:warptsd:1286540878545948715>"
e_blank = ":stop_button:"
e_bomb = "<:laddawan:1286535333546295409>"

# Decode base64 twice
TOKEN = str(DECODE(DECODE(
    b'VFZSSk5FMVVVVEpQVkVFeFRXcE5ORTVFUlRSTmFrazBUV2N1UjFaMFN6VkpMamhKUlZZNWFEaGhOWFJrVkdkSFpYbEpVMHA1VG5wT1VuQnVOMVpwYVhwSloyNTJlVVZ6')))[
        2:-1]
#client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.command()
async def start(ctx, difficulty: str = ''):
    if difficulty == '':
        await ctx.send("Select a difficulty (easy, medium, hard, impossible)")
    elif not difficulty in LEVELS:
        await ctx.send('https://giphy.com/gifs/latelateshow-james-corden-late-show-3o85g2ttYzgw6o661q')


    size = LEVELS[difficulty]['size']
    bombs = LEVELS[difficulty]['bombs']
    current_revealed = [[False for _ in range(size)] for _ in range(size)]
    await ctx.send(f'{":stop_button:" * size}\n' * size)

@bot.command()
async def select(ctx, x: int, y: int):
    x -= 1
    y -= 1
    current_board = generate_board(size,bombs,y,x)
    check_cell(current_board, current_revealed, y,x)




@bot.command()
async def rickroll(ctx):
    os.system('"C:\Program Files\Google\Chrome\Application\chrome.exe" https://www.youtube.com/watch?v=xvFZjo5PgG0')

@bot.command()
async def lose(ctx):
    await ctx.send(get_random_gif_url())



@bot.command()
async def ornok(ctx, num1=1):
    await ctx.send("<:laddawan:1286535333546295409>"*num1)



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
