import random
import requests
import discord
from discord.ext import commands

class Arkhamdb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cards = self._get_cards()

    def _get_cards(self):
        return requests.get(
            'https://www.arkhamdb.com/api/public/cards?encounter=1').json()

    # creates embedded link with card image
    def _embed_card(self, card, image=True):
        e = discord.Embed()
        if image and card.get('imagesrc', None):
            image_url = "https://www.arkhamdb.com" + card.get('imagesrc')
            e.set_image(url=image_url)
        e.url = card.get('url', None)
        e.title = card.get('name', None)
        if card.get('xp', 0):
            e.title += " (" + str(card.get('xp', '-')) + ")"
        if card.get('subname', None):
            e.description = card.get('subname')
        return e

    async def _embed_deck(self, message):
        content = message.content.lower()
        # parse message to get deck id and type (decklist or deck)
        deckId = None
        deckType = None
        if "arkhamdb.com/deck/view/" in content:
            deckId = re.search('(?<=arkhamdb.com/deck/view/)(.{6})', content)
            deckType = 'deck'
        if "https://arkhamdb.com/decklist/" in content:
            deckId = re.search('(?<=arkhamdb.com/decklist/view/)(.{5})', content)
            deckType = 'decklist'

        if deckId:
            # get deck from arkhamdb api
            deckId = deckId.group()
            if deckType == 'deck':
                apiString = 'https://arkhamdb.com/api/public/deck/' + deckId
            if deckType == 'decklist':
                apiString = 'https://arkhamdb.com/api/public/decklist/' + deckId
            deckJson = requests.get(apiString).json()
            # create initial embed using investigator card image
            gator = list(filter(lambda card: card.get('code', 0) == deckJson.get('investigator_code', None), cards))[0]
            e = discord.Embed()
            e.description = ''
            # set title to deck name with appropriate url
            e.title = deckJson.get('name', "") + " " + deckJson.get('version', "")
            if deckType == 'deck':
                e.url = 'https://arkhamdb.com/deck/view/' + deckId
            if (deckType == 'decklist'):
                e.url = 'https://arkhamdb.com/decklist/view/'+ deckId
            categories = ['Asset', 'Permanent', 'Event', 'Skill', 'Treachery']
            deckCards = list(filter(lambda card: card.get('code', '') in deckJson.get('slots', {}).keys(), cards))
            for category in categories:
                if(category == 'Permanent'):
                    categoryCards = list(filter(lambda card: card.get('permanent', False) == True, deckCards))
                else:
                    categoryCards = list(filter(lambda card: card.get('type_code', '') == category.lower() and card.get('permanent', False) == False, deckCards))
                if(category == 'Treachery'):
                    e.description += '\n' + 'Treacheries:'
                else:
                    e.description += '\n ' + category + 's:'
                for card in categoryCards:
                    cardString = str(deckJson.get('slots')[card.get('code')]) + 'x '
                    cardString += card.get('name', '')
                    if card.get('xp', 0) > 0:
                        cardString += ' (' + str(card.get('xp', 0)) + ')'
                    e.description += '\n' + cardString
                e.description += '\n'
            await message.channel.send(embed=e)
        else:
            await message.channel.send('Deck URL detected, unable to extract deck ID')

    @commands.command()
    async def refresh(self, ctx):
        self.cards = self._get_cards()
        await ctx.send('Card pool refreshed')

    @commands.command()
    async def upgrade(self, ctx, target):
        targets = list(filter(lambda card: card.get('name', "").lower() == target.lower() and card.get('xp', 0) is not 0, self.cards))
        if len(targets):
            e = self._embed_card(random.choice(list(targets)))
            await ctx.send(embed=e)
        else:
            await ctx.send("No matches for " + target)

    @commands.command()
    async def weakness(self, ctx, *args):
        weaknesses = list(filter(lambda card: card.get('subtype_code', None) ==
                                'basicweakness' and card.get('name', "") is not "Random Basic Weakness", self.cards))
        if len(list(args)):
            def matchTraits(card):
                matches = 0
                for trait in list(args):
                    if trait.lower() in card.get('traits', '').lower():
                        matches += 1
                if matches > 0:
                    return True
                return False

            weaknesses = filter(matchTraits, weaknesses)
        weakness = random.choice(list(weaknesses))
        e = self._embed_card(weakness)
        await ctx.send(embed=e)

    @commands.command()
    async def card(self, ctx, *args):
        if(len(list(args)) == 0):
            name = 'ancient evils'
        else:
            name = ' '.join(list(args))
        matches = list(filter(lambda card: name.lower() in card.get('name', '').lower(), self.cards))
        if len(matches) and len(matches) <= 3:
            for match in matches:
                e = self._embed_card(match)
                await ctx.send(embed=e)
        elif len(matches) > 3 and len(matches) <= 10:
            for match in matches:
                e = self._embed_card(match, False)
                await ctx.send(embed=e)
        elif len(matches) > 10:
            await ctx.send('More than 10 matches, please refine your search')
        else:
            await ctx.send('No matches')

    @commands.command()
    async def investigator(self, ctx, faction=None):
        investigators = list(filter(lambda card: card.get('type_code', '') == 'investigator' and card.get('permanent', True) and card.get('hidden', True), self.cards))
        if faction:
            investigators = list(filter(lambda card: card.get('faction_code', '') == faction.lower(), investigators))
        if len(investigators) > 0:
            choice = random.choice(list(investigators))
            e = self._embed_card(choice)
            await ctx.send(embed=e)
        else:
            await ctx.send('No matches found - invalid faction')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if "arkhamdb.com/deck/view/" in message.content.lower() or 'arkhamdb.com/decklist/view/' in message.content.lower():
            await self._embed_deck(message)