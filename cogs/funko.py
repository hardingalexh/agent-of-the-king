import random
import discord
from discord.ext import commands

class Funko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.shield = u'\U0001F6E1'
        self.boom = u"\U0001F4A5"
        self.ex =  "!!!"
        self.standard = [self.shield, self.shield, self.boom, self.boom, self.boom, self.ex]
        self.special = {
            'chaos': ['Blank', 'Blank', 'Blank', self.ex, self.ex, self.ex],
            'champion': [self.shield, self.shield, self.shield, self.shield, self.ex, self.ex]
        }
    
    @commands.command(usage="<quantity> <any number of special dice>", help="Rolls dice for the funkoverse strategy game. The first argument is a number and will roll that many standard dice. Any further arguments must be valid special dice.")
    async def funko(self, ctx, *args):
        args = list(args)
    
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
                e.description += '\n' + random.choice(self.standard)

        if len(args) > 1:
            args.pop(0)
            for arg in args:
                if arg.lower() in self.special.keys():
                    e.description += '\n \n' + arg.lower().capitalize() + ' Die:'
                    e.description += '\n' + random.choice(self.special.get(arg.lower()))
                else:
                    await ctx.send(arg + ' is not a valid special die. Valid special dice are: ' + ', '.join(self.special.keys()))
        await ctx.send(embed=e)
