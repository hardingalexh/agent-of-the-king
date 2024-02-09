import re
import discord
from discord.ext import commands

class Dad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        r_search = re.search(r'(?:i\'m|i am)\s(.*?)(?:\.|!|\?|$)', message.content, re.IGNORECASE)
        if r_search and r_search.group(1) and not message.author.bot:
            await message.channel.send(f"Hi {r_search.group(1)}, I'm Agent of the King!")
            await message.author.edit(nick=r_search.group(1))