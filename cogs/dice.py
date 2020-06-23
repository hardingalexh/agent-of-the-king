import random
import discord
from discord.ext import commands

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    ## Dice commands
    @commands.command()
    async def cointoss(self, ctx):
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command()
    async def roll(self, ctx, dice):
        split = dice.lower().split('d')
        if split[0] == '':
            split[0] = 1
        try:
            q = int(split[0])
            d = int(split[1])
        except:
            await ctx.send("Invalid die type or quantity")
            return

        if q > 100 or d > 100:
            await ctx.send("I can only count to 100 on either hand. Try again with 100 or less dice/sides.")
        else:
            rolls = []
            for i in range(q):
                rolls.append(random.randrange(1, d+1))
            e = discord.Embed()
            e.title= 'Roll ' + dice
            e.description = ''
            if len(rolls) > 2:
                e.description += 'High Roll: ' + str(max(rolls)) + '\n'
                e.description += 'Low Roll: ' + str(min(rolls)) + '\n'
            e.description += 'Total: ' + str(sum(rolls)) + '\n'
            e.description += '\n Rolls:'
            for roll in rolls:
                e.description += '\n' + str(roll)

            await ctx.send(embed=e)

    @commands.command()
    async def pickone(self, ctx, *args):
        await ctx.send(random.choice(args))
    
    @commands.command()
    async def funko(self, ctx, quantity, character=None):
        shield = u'\U0001F6E1'
        boom = u"\U0001F4A5"
        ex =  u"\u2757" + u"\u2757" + u"\u2757"
        faces = [shield, shield, boom, boom, boom, ex]
        if character and character.lower() == 'jeff':
            faces = ['', '', '', ex, ex, ex]
        e = discord.Embed()
        e.title = "Funkoverse Strategy Game Dice Roll"
        e.description = ''
        for roll in range(int(quantity)):
            e.description += '\n' + random.choice(faces)
        await ctx.send(embed=e)
