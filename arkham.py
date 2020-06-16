import os
import random
import re
import requests

import discord
from discord.ext import commands

from cogs.arkhamdb import Arkhamdb
from cogs.dice import Dice

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.Client()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_message(message):
    if 'hastur' in message.content.lower():
        await message.channel.send(message.author.name + ' takes 1 horror')
    if ':skull:' in message.content.lower():
        await message.channel.send(u"\U0001F3BA" + u"doot doot" + u"\U0001F3BA")
    if 'x' == message.content.lower():
        await message.channel.send('JASON')
    
    await bot.process_commands(message)

bot.add_cog(Arkhamdb(bot))
bot.add_cog(Dice(bot))
bot.run(token)
