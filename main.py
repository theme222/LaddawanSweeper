# bot.py
import os
import discord
from pybase64 import standard_b64decode as DECODE
from discord.ext import commands
from discord import app_commands
from laddawan import *
import requests
import random

current_game = Game()

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

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


def display_board(game, show_all=False):
    rows_per_msg = 30 // game.sizeX
    output = []

    for row in game.board:
        txt_row = ""
        for tile in row:
            txt_row += tile.get_emoji(show_all)
        output.append(txt_row)

    new_output = ['']
    current = 0
    cycle = 0
    for row in output:
        if cycle < rows_per_msg:
            new_output[current] += f'{row}\n'
            cycle += 1
        else:
            cycle = 0
            current += 1
            new_output.append('')

    return new_output


@bot.command()
async def start(ctx, difficulty: str = ''):
    global current_game
    if difficulty == '':
        await ctx.send("Select a difficulty (easy, medium, hard, impossible, custom)")
        return
    elif not difficulty in LEVELS and difficulty != "custom":
        await ctx.send('https://giphy.com/gifs/latelateshow-james-corden-late-show-3o85g2ttYzgw6o661q')
        return

    size = LEVELS[difficulty]['size']
    bombs = LEVELS[difficulty]['bombs']
    current_game = Game(size, size, bombs)

    board = display_board(current_game)
    for msg in board:
        if msg:
            await ctx.send(msg)


@bot.command()
async def select(ctx, x: int, y: int):
    global current_game
    y -= 1
    x -= 1
    if current_game.status in ["Lose", "Win"]:
        await ctx.send("Please start a new game")
        return
    if current_game.status == "NotStarted":
        current_game.first_move(y, x)
    else:
        current_game.check_cell(y, x)

    if current_game.status == "Lose":
        board = display_board(current_game, show_all=True)
        for msg in board:
            if msg: await ctx.send(msg)
        await ctx.send("https://giphy.com/gifs/travisband-l-travis-fran-healy-ZDst1zdFKc5WTAr991")
        return
    if current_game.status == "Win":
        board = display_board(current_game,show_all=True)
        for msg in board:
            if msg: await ctx.send(msg)
        await ctx.send("https://giphy.com/gifs/yhw-your-happy-workplace-happiness-consultant-Qadbv0ccmSrJL9Vlwj")
        return


    board = display_board(current_game)
    for msg in board:
        if msg: await ctx.send(msg)


@bot.command()
async def ornok(ctx, num1=1):
    await ctx.send("<:laddawan:1286535333546295409>" * num1)


@bot.command()
async def sync_commands(ctx):
    await ctx.send("syncing")
    await bot.tree.sync()


def get_random_gif_url(limit=10):
    params = {
        'api_key': str(DECODE(DECODE(b'VTNKMFFqUTViMjh6TjA1Sk0zSndPVkZrUlVoWVVUVnpiRW8yVFVsM1oyWT0=')))[2:-1],
        'tag': '',
        "q": 'explosion',
        'limit': limit,  # You can specify a tag to get GIFs related to that tag
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

