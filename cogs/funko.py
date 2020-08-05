import random
import discord
from discord.ext import commands

class Funko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command(usage="<quantity> <any number of special dice>", help="Rolls dice for the funkoverse strategy game. Specify a character for character-specific die rolls.")
    async def funko(self, ctx, *args):
        args = list(args)
        shield = u'\U0001F6E1'
        boom = u"\U0001F4A5"
        ex =  "!!!"
        faces = [shield, shield, boom, boom, boom, ex]
        special = {
            'chaos': ['Blank', 'Blank', 'Blank', ex, ex, ex],
            'champion': [shield, shield, shield, ex, ex, ex]
        }
        e = discord.Embed()
        e.title = "Funkoverse Strategy Game Dice Roll"
        e.description = ''
        try:
            quantity = int(args[0])
        except:
            await ctx.send('First argument must be a valid number')
        
        if quantity > 100:
            await ctx.send("I can only count to 100 on either hand. Try again with 100 or less dice.")
            return

        for roll in range(quantity):
                e.description += '\n' + random.choice(faces)

        if len(args) > 1:
            args.pop(0)
            for arg in args:
                if arg.lower() in special.keys():
                    e.description += '\n \n' + arg + ' Die:'
                    e.description += '\n' + random.choice(special.get(arg.lower().capitalize()))
                else:
                    await ctx.send(arg + 'is not a valid special die.')
        await ctx.send(embed=e)
