import os
import random
import re
import requests

import discord
from discord.ext import commands

from cogs.arkhamdb import Arkhamdb
from cogs.dice import Dice
from cogs.bag import Bag
from cogs.blob import Blob
from cogs.funko import Funko
from cogs.marvelcdb import Marvelcdb
#from cogs.dad import Dad

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
    if 'snowman' in message.content.lower() or 'sexy' in message.content.lower():
        e = discord.Embed()
        e.set_image(url="https://i.imgur.com/8wz9cF6.jpeg")
        await message.channel.send(embed=e)
    
    await bot.process_commands(message)

bot.add_cog(Arkhamdb(bot))
bot.add_cog(Dice(bot))
bot.add_cog(Bag(bot))
bot.add_cog(Blob(bot))
bot.add_cog(Funko(bot))
bot.add_cog(Marvelcdb(bot))
#bot.add_cog(Dad(bot))
bot.run(token)
