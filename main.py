# bot.py
import os
import discord

# VFZSSk5FMVVVVEpQVkVFeFRXcE5ORTVFUlRSTmFrazBUV2N1UjFaMFN6VkpMamhKUlZZNWFEaGhOWFJrVkdkSFpYbEpVMHA1VG5wT1VuQnVOMVpwYVhwSloyNTJlVVZ6
# Decode base64 twice
TOKEN = ''

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run('')
