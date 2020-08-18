import re
import random
import requests
import discord
from discord.ext import commands

class Marvelcdb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cards = self._get_cards()
    
    @commands.group(brief="Defines Marvel cdb functions. ")
    async def m(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Marvel command passed...')

    def _get_cards(self):
        return requests.get(
            'https://www.marvelcdb.com/api/public/cards').json()

    # creates embedded link with card image
    def _embed_card(self, card, image=True):
        e = discord.Embed()
        if image and card.get('imagesrc', None):
            image_url = "https://www.marvelcdb.com" + card.get('imagesrc')
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
        if "marvelcdb.com/deck/view/" in content:
            deckId = re.search('(?<=marvelcdb.com/deck/view/)(.{6})', content)
            deckType = 'deck'
        if "https://marvelcdb.com/decklist/" in content:
            deckId = re.search('(?<=marvelcdb.com/decklist/view/)(.{5})', content)
            deckType = 'decklist'

        if deckId:
            # get deck from marvelcdb api
            deckId = deckId.group()
            if deckType == 'deck':
                apiString = 'https://marvelcdb.com/api/public/deck/' + deckId
            if deckType == 'decklist':
                apiString = 'https://marvelcdb.com/api/public/decklist/' + deckId
            deckJson = requests.get(apiString).json()
            # create initial embed using investigator card image
            gator = list(filter(lambda card: card.get('code', 0) == deckJson.get('investigator_code', None), self.cards))[0]
            e = discord.Embed()
            e.description = ''
            # set title to deck name with appropriate url
            e.title = deckJson.get('name', "") + " " + deckJson.get('version', "")
            if deckType == 'deck':
                e.url = 'https://marvelcdb.com/deck/view/' + deckId
            if (deckType == 'decklist'):
                e.url = 'https://marvelcdb.com/decklist/view/'+ deckId
            categories = ['Upgrade', 'Ally', 'Support', 'Event', 'Resource']
            deckCards = list(filter(lambda card: card.get('code', '') in deckJson.get('slots', {}).keys(), self.cards))
            for category in categories:
                categoryCards = list(filter(lambda card: card.get('type_code', '') == category.lower() and card.get('permanent', False) == False, deckCards))
                if(category == 'Ally'):
                    e.description += '\n' + 'Allies:'
                else:
                    e.description += '\n ' + category + 's:'
                for card in categoryCards:
                    cardString = str(deckJson.get('slots')[card.get('code')]) + 'x '
                    cardString += card.get('name', '')
                    e.description += '\n' + cardString
                e.description += '\n'
            await message.channel.send(embed=e)
        else:
            await message.channel.send('Deck URL detected, unable to extract deck ID')

    @m.command(help="Refreshes the card pool from marvelcdb")
    async def refresh(self, ctx):
        self.cards = self._get_cards()
        await ctx.send('Card pool refreshed')

    @m.command(usage="<search string>", help="Finds and embeds all cards matching your query, up to 10 matches. Embeds a card image if the image exists on marvelcdb.")
    async def card(self, ctx, *, arg):
        if not arg:
            arg = 'MODOK'
        matches = list(filter(lambda card: arg.lower() in card.get('name', '').lower(), self.cards))
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

    @m.command(usage="<search string>", help="Finds and lists all cards with at least one trait matching your query, up to 100 matches.")
    async def trait(self, ctx, *args):
        if len(list(args)):
            def matchTraits(card):
                matches = 0
                for trait in list(args):
                    if trait.lower() in card.get('traits', '').lower():
                        matches += 1
                if matches > 0:
                    return True
                return False
            matched = list(filter(matchTraits, self.cards))
            try:
                e = discord.Embed()
                e.title = "Traits Search: " + ', '.join(list(args))
                e.description = ''
                def faction(e):
                    return e.get('faction_code', '')
                matched.sort(key=faction)
                factions = []
                for match in list(matched):
                    if match.get('faction_code', '') not in factions:
                        e.description += '\n' + match.get('faction_name') + ": \n"
                        factions.append(match.get('faction_code', ''))
                    e.description += match.get('name', '')
                    e.description += '\n'
                await ctx.send(embed=e)
            except:
                await ctx.send('The results of your search are too large for discord. Please try refining your search.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if "marvelcdb.com/deck/view/" in message.content.lower() or 'marvelcdb.com/decklist/view/' in message.content.lower():
            await self._embed_deck(message)
