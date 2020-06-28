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

    async def _setup(self, ctx, param):
        self.players = param
        self.clues = 0
        self.damage = 0
        self.supplies = 0
        await ctx.send('Set up the blob for ' + str(param) + ' players')
        await self._status(ctx)

    async def _status(self, ctx):
        e = discord.Embed()
        e.title = "The Blob That Ate Everything"
        e.description = ""
        e.description += "\n Supplies: " + str(self.supplies)
        e.description += "\n Clues: " + str(self.clues)
        e.description += "\n Damage: " + str(self.damage)
        await ctx.send(embed=e)

    async def _add(self, ctx, cmd, param):
        setattr(self, cmd, getattr(self, cmd) + param)
        await ctx.send(str(param) + ' ' + cmd)
        await self._status(ctx)

    @commands.command()
    async def blob(self, ctx, *args):
        cmd = args[0].lower()
        param = int(args[1]) if len(args) == 2 else 0
        if cmd == 'setup':
           await self._setup(ctx, param)
        elif cmd == 'status':
           await self._status(ctx)
        elif cmd in ['supplies', 'damage', 'clues']:
           await self._add(ctx, cmd, param)
