# bot.py
import os
import discord
from pybase64 import standard_b64decode as DECODE

# Decode base64 twice
TOKEN = str(DECODE(DECODE(
    b'VFZSSk5FMVVVVEpQVkVFeFRXcE5ORTVFUlRSTmFrazBUV2N1UjFaMFN6VkpMamhKUlZZNWFEaGhOWFJrVkdkSFpYbEpVMHA1VG5wT1VuQnVOMVpwYVhwSloyNTJlVVZ6')))[
        2:-1]
client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(msg):
    await msg.channel.send("Test")


client.run(TOKEN)
