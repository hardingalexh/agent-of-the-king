import random
import discord
from discord.ext import commands

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    ## Dice commands
    @commands.command(help="Returns heads or tails")
    async def cointoss(self, ctx):
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command(usage="<XdY>", help="Rolls X dice of Y sides. For example, !roll 3d6 will roll 3 D6s. If a number of dice is not specified, 1 roll will be made. For example, !roll d6 will roll a single d6.")
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
            if sum(rolls) == 69:
                await ctx.send("_nice_")

    @commands.command(usage="[any number of space separated things]", help="Chooses one from the list provided")
    async def pickone(self, ctx, *args):
        await ctx.send(random.choice(args))