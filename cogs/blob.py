import discord
import math
from datetime import datetime
from datetime import timedelta
from discord.ext import commands

class Blob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.players = 0
        self.clues = 0
        self.damage = 0
        self.countermeasures = 0
        self.endtime = 0
    
    @commands.group(brief="Manages state for playing the blob that ate everything, using multiple commands. Type !help blob for more info.")
    async def blob(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid blob command passed...')

    @blob.command(usage="<player count>", help="Sets up a new blob scenario for the given player count")
    async def setup(self, ctx, param):
        self.players = int(param)
        self.clues = 0
        self.damage = 0
        self.countermeasures = math.ceil(int(param) / 2)
        self.endtime = datetime.now() + timedelta(seconds=60*180)
        await ctx.send('Set up the blob for ' + str(param) + ' players')
        await self.status(ctx)

    @blob.command(help="Prints the status of the current blob event")    
    async def status(self, ctx):
        e = discord.Embed()
        timeremaining = self.endtime - datetime.now()
        if timeremaining.days < 0:
            timeremainingString = '0'
        else:
            timeremainingString = str(math.floor(timeremaining.seconds / 60))
        e.title = "The Blob That Ate Everything"
        e.description = ""
        if self.damage >= self.players * 15:
            e.description += "The blob is defeated - the investigators win!"
        elif timeremaining.days < 0:
            e.description += "The blob was not defeated in time - the investigators lose!"

        e.description += "\n Time Remaining: " + timeremainingString + ' Minutes '
        e.description += "(Ends at " + self.endtime.strftime("%I:%M %p") + ")"
        e.description += "\n Countermeasures: " + str(self.countermeasures)
        e.description += "\n Clues: " + str(self.clues) + '/' + str(self.players * 2)
        e.description += "\n Damage: " + str(self.damage) + '/' + str(self.players * 15)
        await ctx.send(embed=e)

    @blob.command(usage="<quantity>", help="Adds or subtracts the given number of countermeasures. For example, !blob countermeasures 1 adds 1 supply, !blob countermeasures -3 removes 3 countermeasures.")
    async def countermeasures(self, ctx, quantity):
        await self._add(ctx, 'countermeasures', quantity)
    
    @blob.command(usage="<quantity>", help="Adds or subtracts the given number of damage. For example, !blob damage 1 adds 1 supply, !blob damage -3 removes 3 damage.")
    async def damage(self, ctx, quantity):
        await self._add(ctx, 'damage', quantity)
    
    @blob.command(usage="<quantity>", help="Adds or subtracts the given number of clues. For example, !blob clues 1 adds 1 supply, !blob clues -3 removes 3 clues.")
    async def clues(self, ctx, quantity):
        await self._add(ctx, 'clues', quantity)
    
    async def _add(self, ctx, category, quantity):
        category = category.lower()
        if category not in ['countermeasures', 'clues', 'damage']:
            await ctx.send(category + ' is not a valid category. Try again with countermeasures, damage or clues.')    
            return
        if getattr(self, category) + int(quantity) < 0:
           await ctx.send('Invalid command: ' + category + " can't be reduced below 0")
           return
        setattr(self, category, getattr(self, category) + int(quantity))
        await ctx.send(str(quantity) + ' ' + category)
        await self.status(ctx)
        if category == 'damage' and self.damage >= int(self.players) * 15:
            await ctx.send('The blob is defeated! The investigators win!')
