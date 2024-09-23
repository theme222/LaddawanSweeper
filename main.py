# bot.py
import os
import discord
from pybase64 import standard_b64decode as DECODE
from discord.ext import commands
from discord import app_commands
from laddawan import *
import requests
import random

current_games = {}  # key(channel id), value(Game object)

LEVELS = {
    'easy': {'size': 5, 'bombs': 4},  # 16% bomb
    'medium': {'size': 7, 'bombs': 9},  # 18% bomb
    'hard': {'size': 10, 'bombs': 20},  # 20% bomb
    'impossible': {'size': 12, 'bombs': 32}  # 22% bomb
}

PREFIX = "$"

# Decode base64 twice
TOKEN = str(DECODE(DECODE(
    b'VFZSSk5FMVVVVEpQVkVFeFRXcE5ORTVFUlRSTmFrazBUV2N1UjFaMFN6VkpMamhKUlZZNWFEaGhOWFJrVkdkSFpYbEpVMHA1VG5wT1VuQnVOMVpwYVhwSloyNTJlVVZ6')))[
        2:-1]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


def get_game(ctx):
    if str(ctx.channel.id) in current_games:
        return current_games[str(ctx.channel.id)]
    else:
        return None


def delete_game(ctx):
    if str(ctx.channel.id) in current_games:
        del current_games[str(ctx.channel.id)]


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
            cycle = 1
            current += 1
            new_output.append(f'{row}\n')

    return new_output


@bot.event
async def on_message(message):
    if str(message.channel.id) in current_games and not message.author.bot:
        msg = message.content.split()
        if len(msg) == 2:
            try:
                x = int(msg[0])
                y = int(msg[1])
                ctx = await bot.get_context(message)
                await ctx.invoke(bot.get_command("select"), x, y)
            except ValueError:
                pass

    # This is important to allow other commands to work
    await bot.process_commands(message)


@bot.command()
async def start(ctx, difficulty: str = ''):
    global current_games

    channel_id = ctx.channel.id
    if difficulty == '':
        await ctx.send("Select a difficulty (easy, medium, hard, impossible)")
        return
    elif not (difficulty in LEVELS) and difficulty != "custom":
        await ctx.send('https://giphy.com/gifs/latelateshow-james-corden-late-show-3o85g2ttYzgw6o661q')
        return

    size = LEVELS[difficulty]['size']
    bombs = LEVELS[difficulty]['bombs']
    current_games[str(channel_id)] = Game(size, size, bombs)

    board = display_board(current_games[str(channel_id)])
    for msg in board:
        if msg:
            await ctx.send(msg)


@bot.command()
async def select(ctx, x: int, y: int):
    current_game = get_game(ctx)

    if current_game is None or current_game.status in ["Lose", "Win", "Uninitialized"]:
        await ctx.send("Please start a new game")
        return

    y -= 1
    x -= 1

    if not current_game.valid_move(y, x):
        await ctx.send("Invalid position")
        return

    if current_game.status == "NotStarted":
        current_game.first_move(y, x)
    else:
        current_game.check_cell(y, x)

    if current_game.status == "Lose":
        board = display_board(current_game, show_all=True)
        for msg in board:
            if msg: await ctx.send(msg)
        delete_game(ctx)
        await ctx.send("https://giphy.com/gifs/travisband-l-travis-fran-healy-ZDst1zdFKc5WTAr991")
        return
    if current_game.status == "Win":
        board = display_board(current_game, show_all=True)
        for msg in board:
            if msg: await ctx.send(msg)
        delete_game(ctx)
        await ctx.send("https://giphy.com/gifs/yhw-your-happy-workplace-happiness-consultant-Qadbv0ccmSrJL9Vlwj")
        return

    board = display_board(current_game)
    for msg in board:
        if msg: await ctx.send(msg)


@bot.command()
async def flag(ctx, x: int, y: int):
    current_game = get_game(ctx)

    if current_game is None or current_game.status in ["Lose", "Win", "Uninitialized"]:
        await ctx.send("Please start a new game")
        return

    y -= 1
    x -= 1

    if not current_game.valid_move(y, x):
        await ctx.send("Invalid position")
        return

    current_game.flag(y, x)

    board = display_board(current_game)
    for msg in board:
        if msg: await ctx.send(msg)


@bot.command()
async def surrender(ctx):
    current_game = get_game(ctx)
    if current_game:
        current_game.lose()
        board = display_board(current_game, show_all=True)
        for msg in board:
            if msg: await ctx.send(msg)
        await ctx.send("https://giphy.com/gifs/muppets-the-muppet-show-statler-and-waldorf-kzuNhxVf27plttAS7E")
        delete_game(ctx)
        return
    else:
        await ctx.send("No games to surrender")


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Info", description="", color=0x62a0ea)
    embed.set_author(name="Laddawan Sweeper", url="https://www.youtube.com/watch?v=iik25wqIuFo",
                     icon_url="https://cdn.discordapp.com/attachments/1281468020245663779/1286535257063030794/image.png?ex=66ef9453&is=66ee42d3&hm=c2d008690bbeee4d3331acc1ed72a17d8788d1eff758fa107b0007555ad86aaa&")
    embed.add_field(name="Start {difficulty}",
                    value="Start a game of Laddawan Sweeper™.\ndifficulty : easy (5x5), medium(7x7), hard(10x10), impossible(12x12) \nThese games are unique to their specific channel in which you run the command from.",
                    inline=False)
    embed.add_field(name="Select {x} {y}",
                    value="Select a position to check.\nx : The x position (column)\ny : The y position (row)\n( You can also type two numbers with a space in the same channel to run this command as well )",
                    inline=False)
    embed.add_field(name="Flag {x} {y}",
                    value="Select a position to flag.\nx : The x position (column)\ny : The y position (row)",
                    inline=False)
    embed.add_field(name="Surrender", value="Surrender the game", inline=True)
    embed.add_field(name="Help", value="Help menu", inline=True)
    embed.set_footer(text="made in satit kaset")
    await ctx.send(embed=embed)


@bot.command()
async def ornok(ctx, num1=1):
    await ctx.send("<:laddawan:1286535333546295409>" * num1)


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
