import os
import random
import re
import requests
import discord

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

cards = []

# gets all cards including encounters


def get_cards():
    global cards
    cards = requests.get(
        'https://www.arkhamdb.com/api/public/cards?encounter=1').json()

# creates embedded link with card image


def embed_card(card, image=True):
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


# Commenting out arkhamdb bot skeleton - waiting on arkhamdb to resolve TLS issues
client = discord.Client()
bot = commands.Bot(command_prefix='!')


@bot.command(name='refresh')
async def refresh_cards(ctx):
    get_cards()
    await ctx.send('Card pool refreshed')


@bot.command(name='upgrade')
async def get_random_upgraded_card(ctx, target):
    targets = list(filter(lambda card: card.get('name', "").lower() == target.lower() and card.get('xp', 0) is not 0, cards))
    if len(targets):
        e = embed_card(random.choice(list(targets)))
        await ctx.send(embed=e)
    else:
        await ctx.send("No matches for " + target)

@bot.command(name='weakness')
async def get_random_basic_weakness(ctx, *args):
    weaknesses = list(filter(lambda card: card.get('subtype_code', None) ==
                             'basicweakness' and card.get('name', "") is not "Random Basic Weakness", cards))
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
    e = embed_card(weakness)
    await ctx.send(embed=e)


@bot.command(name='card')
async def search_card(ctx, name="Ancient Evils", level=None):
    def query(card):
        return (name.lower() in card.get('name', '').lower()) and (str(card.get('xp', '')) == level or level is None)
    matches = list(filter(query, cards))
    if len(matches) and len(matches) <= 3:
        for match in matches:
            e = embed_card(match)
            await ctx.send(embed=e)
    elif len(matches) > 3 and len(matches) <= 10:
        for match in matches:
            e = embed_card(match, False)
            await ctx.send(embed=e)
    elif len(matches) > 10:
        await ctx.send('More than 10 matches, please refine your search')
    else:
        await ctx.send('No matches')

async def embed_deck(message):
    content = message.content.lower()
    deckId = None
    deckType = None
    if "arkhamdb.com/deck/view/" in content:
        deckId = re.search('(?<=arkhamdb.com/deck/view/)(.{6})', content)
        deckType = 'deck'
    if "https://arkhamdb.com/decklist/" in content:
        deckId = re.search('(?<=arkhamdb.com/decklist/view/)(.{5})', content)
        deckType = 'decklist'
    
    if deckId:
        deckId = deckId.group()
        if deckType = 'deck':
            apiString = 'https://arkhamdb.com/api/public/deck/' + deckId
        if deckType = 'decklist':
            apiString = 'https://arkhamdb.com/api/public/decklist/' + deckId
        deckJson = requests.get(apiString).json()
        gator = list(cards.filter(lambda card: card.get('id', 0) == deckJson.get('investigator_code', None)))[0]
        e = embed_card(gator)
        message.channel.send(embed=e)
    else:
        await message.channel.send('Deck URL detected, unable to extract deck ID')

@bot.event
async def on_message(message):
    if 'hastur' in message.content.lower():
        await message.channel.send(message.author.name + ' takes 1 horror')
    if ':skull:' in message.content.lower():
        await message.channel.send(u"\U0001F3BA" + u"doot doot" + u"\U0001F3BA")
    if 'x' == message.content.lower():
        await message.channel.send('JASON')
    if "arkhamdb.com/deck/view/" in message.content.lower() or 'arkhamdb.com/decklist/view/' in message.content.lower():
        await embed_deck(message)
    
    await bot.process_commands(message)

get_cards()
bot.run(token)
