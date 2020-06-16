import random
import requests
import discord
from discord.ext import commands
import discord

class Bag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.bag = []
        self.revealed = []
        self.valid = ['+1', '0', '-1', '-2', '-3', '-4', '-5', '-6', '-7', '-8', 'skull', 'cultist', 'tablet', 'elder-thing', 'elder-sign', 'auto-fail']

    def _emoji(self, token):
        lookup = {
            'skull': ':skull-1:',
            'cultist': ':cultist:',
            'tablet': ':tablet:',
            'elder-thing': ':tentacles:',
            'elder-sign': ':eldersign:',
            'auto-fail': ':autofail:'
        }
        return lookup.get(token, token)

    async def _add_to_bag(self, ctx, args):        
        args = list(args)
        del args[0]
        accepted = []
        rejected = []
        for token in args:
            if token.lower() in self.valid:
                self.bag.append(token)
                accepted.append(token)
            else:
                rejected.append(token)
        if len(accepted):
            self.bag.sort()
            accString = ','.join(accepted)
            await ctx.send('Succesfully added the following tokens: ' + accString)
        if len(rejected):
            rejString = ','.join(rejected)
            await ctx.send('Failed to add the following invalid tokens: ' + rejString)

    async def _clear_bag(self, ctx):
        self.bag.clear()
        await ctx.send('Bag Cleared')
    
    async def _list_bag(self, ctx):
        self.bag.sort()
        e = discord.Embed()
        e.title = 'Bag Contents'
        e.description = ''
        for token in self.bag:
            e.description = '\n' + self._emoji(token)
        await ctx.send(embed=e)
    
    async def _list_revealed_tokens(self, ctx):
        if len(self.revealed) == 0:
            await ctx.send('There are no revealed tokens')
        else:
            e = discord.Embed()
            e.title = "Currently Revealed Tokens"
            e.description = ''
            for token in self.revealed:
                e.description += '\n' + self._emoji(token)
            await ctx.send(embed=e)

    async def _draw_token(self, ctx, args):
        args = list(args)
        del args[0]
        revealed = []
        numTokens = 1
        if len(args):
            numTokens = int(args[0])
        if numTokens > len(self.bag):
            await ctx.send('There are no tokens in the bag')
            return

        for num in range(numTokens):
            token = random.choice(self.bag)
            revealed.append(token)
            self.revealed.append(token)
            self.bag.remove(token)
        
        e = discord.Embed()
        e.title = 'Bag Draw'
        e.description = 'Revealed the following Token(s): '
        for token in revealed:
            e.description += '\n' + self._emoji(token)
        e.description += '\n' + 'There are currently ' + str(len(self.revealed)) + ' revealed tokens'
        await ctx.send(embed=e)

    async def _return_tokens(self, ctx, args):
        args = list(args)
        del args[0]
        if len(self.revealed) == 0:
            await ctx.send('There are no revealed tokens to return')
            return

        if len(args) == 0:
            for token in self.revealed:
                self.bag.append(token)
            self.bag.sort()
            self.revealed.clear()
            await ctx.send('Returned all tokens to the bag')
        else:
            returned = []
            rejected = []
            for arg in args:
                arg = arg.lower()
                if arg in self.revealed:
                    self.bag.append(arg)
                    self.returned.append(self._emoji(arg))
                    self.revealed.remove(arg)
                else:
                    rejected.append(self._emoji(arg))
            if len(returned) > 0:
                retString = ','.join(returned)
                await ctx.send('Returned the following token(s) to the bag: ' + retString)
            if len(rejected) > 0:
                rejString = ','.join(rejected)
                await ctx.send('The following tokens were not revealed, and therefore could not be returned to the bag: ' + rejString)
            
    @commands.command()
    async def bag(self, ctx, *args):
        cmd = args[0].lower()
        if cmd == 'add':
            await self._add_to_bag(ctx, args)
        elif cmd == 'clear':
            await self._clear_bag(ctx)
        elif cmd == 'list':
            await self._list_bag(ctx)
        elif cmd == 'draw':
            await self._draw_token(ctx, args)
        elif cmd == 'revealed':
            await self._list_revealed_tokens(ctx)
        elif cmd == 'return':
            await self._return_tokens(ctx, args)
