import random
import discord
from discord.ext import commands

class Funko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command(usage="<quantity> <character (optional)", help="Rolls dice for the funkoverse strategy game. Specify a character for character-specific die rolls.")
    async def funko(self, ctx, quantity, character=None):
        shield = u'\U0001F6E1'
        boom = u"\U0001F4A5"
        ex =  "!!!"
        faces = [shield, shield, boom, boom, boom, ex]
        jeffFaces = ['Blank', 'Blank', 'Blank', ex, ex, ex]
        e = discord.Embed()
        e.title = "Funkoverse Strategy Game Dice Roll"
        e.description = ''
        quantity = int(quantity)

        if quantity > 100:
            await ctx.send("I can only count to 100 on either hand. Try again with 100 or less dice.")
            return

        for roll in range(int(quantity)):
            if roll == 0 and character and character.lower() == 'jeff':
                e.description += '\n' + random.choice(jeffFaces)
            else:
                e.description += '\n' + random.choice(faces)
        await ctx.send(embed=e)
