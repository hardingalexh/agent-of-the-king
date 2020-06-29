import discord
from discord.ext import commands

class Blob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.players = 0
        self.clues = 0
        self.damage = 0
        self.supplies = 0
    
    @commands.group(brief="Manages state for playing the blob that ate everything, using multiple commands. Type !help blob for more info.")
    async def blob(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid blob command passed...')

    @blob.command(usage="<player count>", help="Sets up a new blob scenario for the given player count")
    async def setup(self, ctx, param):
        self.players = param
        self.clues = 0
        self.damage = 0
        self.supplies = 0
        await ctx.send('Set up the blob for ' + str(param) + ' players')
        await self.status(ctx)

    @blob.command(help="Prints the status of the current blob event")    
    async def status(self, ctx):
        e = discord.Embed()
        e.title = "The Blob That Ate Everything"
        e.description = ""
        e.description += "\n Supplies: " + str(self.supplies)
        e.description += "\n Clues: " + str(self.clues)
        e.description += "\n Damage: " + str(self.damage)
        await ctx.send(embed=e)

    @blob.command(usage="<supplies/damage/clues> X", help="Adds or subtracts the number of the specified context. For example, !blob supplies 2 or !blob supplies +2 would add 2 supplies, !blob supplies -2 would remove 2 supplies.")
    async def add(self, ctx, category, quantity):
        category = category.lower()
        if category not in ['supplies', 'clues', 'damage']:
            await ctx.send(category + ' is not a valid category. Try again with supplies, damage or clues.')    
            return
        setattr(self, category, getattr(self, category) + int(quantity))
        await ctx.send(str(quantity) + ' ' + category)
        await self.status(ctx)
