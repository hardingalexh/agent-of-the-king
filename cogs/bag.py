import random
import discord
from discord.ext import commands
from discord.utils import get


class Bag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.bag = []
        self.revealed = []
        self.valid = ['+1', '0', '-1', '-2', '-3', '-4', '-5', '-6', '-7', '-8', 'skull', 'cultist', 'tablet', 'elder-thing', 'elder-sign', 'auto-fail']
    
    @commands.group(brief="Manages state for an arkham chaos bag. Type !bag help for further info.")
    async def bag(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid blob command passed...')

    def _emoji(self, token):
        lookup = {
            'skull': "<:skulltoken:626909205177303060>",
            'cultist': "<:cultist:626909205206532106>",
            'tablet': "<:tablet:626909205227503616>",
            'elder-thing': "<:tentacles:626909205189885963>",
            'elder-sign': "<:eldersign:626909205152137216>",
            'auto-fail': "<:autofail:626909204954742784>"
        }
        return lookup.get(token, False) or token

    @bag.command(usage="[space separated tokens]", help="Adds a space-separated list of tokens to the bag. Symbol tokens are called skull, cultist, tablet, elder-thing, elder-sign and auto-fail")
    async def add(self, ctx, *args):
        accepted = []
        rejected = []
        for token in args:
            if token.lower() in self.valid:
                self.bag.append(token)
                accepted.append(self._emoji(token))
            else:
                rejected.append(token)
        if len(accepted):
            self.bag.sort()
            accString = ','.join(accepted)
            await ctx.send('Succesfully added the following tokens: ' + accString)
        if len(rejected):
            rejString = ','.join(rejected)
            await ctx.send('Failed to add the following invalid tokens: ' + rejString)

    @bag.command(usage="[space separated tokens]", help="Removes a space-separated list of tokens from the bag. Symbol tokens are called skull, cultist, tablet, elder-thing, elder-sign and auto-fail")
    async def remove(self, ctx, *args):
        accepted = []
        rejected = []
        for token in args:
            if token.lower() in self.bag:
                self.bag.remove(token.lower())
                accepted.append(token.lower())
            else:
                rejected.append(token.lower())
        if len(accepted):
           accString = ','.join(accepted)
           await ctx.send('Sucessfully removed the following tokens: ' + accString)
        if len(rejected):
           rejString = ','.join(rejected)
           await ctx.send('Failed to remove the following tokens: ' + rejString)

    @bag.command(help="Clears all tokens from the bag")
    async def clear(self, ctx):
        self.bag.clear()
        await ctx.send('Bag Cleared')
    
    @bag.command(name="list", help="Lists all tokens currently in the bag")
    async def _list(self, ctx):
        self.bag.sort()
        e = discord.Embed()
        e.title = 'Bag Contents'
        e.description = ''
        print(self.bag)
        for token in self.bag:
            e.description += '\n' + self._emoji(token)
        await ctx.send(embed=e)
    
    @bag.command(help="Lists all tokens currently revealed")
    async def revealed(self, ctx):
        if len(self.revealed) == 0:
            await ctx.send('There are no revealed tokens')
        else:
            e = discord.Embed()
            e.title = "Currently Revealed Tokens"
            e.description = ''
            for token in self.revealed:
                e.description += '\n' + self._emoji(token)
            await ctx.send(embed=e)

    @bag.command(usage="<quantity, default 1>", help="Draws tokens from the bag, leaving them in the revealed area. If no quantity is listed, it will default to one token. Remember to return to the bag using !bag return after drawing.")
    async def draw(self, ctx, quantity=1):
        revealed = []
        quantity = int(quantity)
        if not quantity:
            await ctx.send('Invalid quantity of tokens')
            return
        
        if quantity > len(self.bag):
            await ctx.send('There are not enough tokens in the bag')
            return

        for num in range(quantity):
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

    @bag.command(name="return", usage="[tokens], default all", help="Returns the specified tokens to the bag from the revealed area. If no tokens are specified, all revealed tokens will be returned.")
    async def _return(self, ctx, *args):
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