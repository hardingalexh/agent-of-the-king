import os
import random
# import requests
import discord

# from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'hastur' in message.content.lower():
        await message.channel.send(message.author.name + ' takes 1 horror')
    
    if 'alejandro' in message.content.lower():
        responses = ['fuck alejandro', 'alejandro is a bitch']
        await message.channel.send(random.choice(responses))

# Commenting out arkhamdb bot skeleton - waiting on arkhamdb to resolve TLS issues
# bot = commands.Bot(command_prefix='!')
# @bot.command(name='weakness')
# async def get_random_basic_weakness(ctx):
#     cards = requests.get('https://www.arkhamdb.com/api/public/cards')
#     await ctx.send(cards)
    

client.run(token)
# bot.run(token)