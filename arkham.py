import os
import discord
from arkhamdb import *
from dice import *
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# gets all cards including encounters
cards = []

@bot.event
async def on_message(message):
    if 'hastur' in message.content.lower():
        await message.channel.send(message.author.name + ' takes 1 horror')
    if ':skull:' in message.content.lower():
        await message.channel.send(u"\U0001F3BA" + u"doot doot" + u"\U0001F3BA")
    if 'x' == message.content.lower():
        await message.channel.send('JASON')
    if "arkhamdb.com/deck/view/" in message.content.lower() or 'arkhamdb.com/decklist/view/' in message.content.lower():
        await embed_deck(message)
    
    await bot.process_commands(message)

get_cards()
print(token)
bot.run(token)
