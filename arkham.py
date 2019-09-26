import os
import random
import requests
import discord

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

cards = []

def get_cards():
    global cards
    cards = requests.get('https://www.arkhamdb.com/api/public/cards?encounter=1').json()

def embed_card(card):
    image_url = "https://www.arkhamdb.com" + card.get('imagesrc', None)
    e = discord.Embed()
    e.set_image(url=image_url)
    e.url = card.get('url', None)
    e.title = card.get('name', None)
    return e

# Commenting out arkhamdb bot skeleton - waiting on arkhamdb to resolve TLS issues
client = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.command(name='refresh')
async def refresh_cards(ctx):
    get_cards()
    await ctx.send('Card pool refreshed')

@bot.command(name='weakness')
async def get_random_basic_weakness(ctx):
    weaknesses = list(filter(lambda card: card.get('subtype_code', None) == 'basicweakness' and card.get('code', "") is not "01000", cards))
    weakness = random.choice(list(weaknesses))
    e = embed_card(weakness)
    await ctx.send(embed=e)

@bot.command(name='card')
async def search_card(ctx, name="Ancient Evils", level=None):
    def query(card):
        return (name.lower() in card.get('name', '').lower()) and (str(card.get('xp', '')) == level or level is None)
    matches = list(filter(query, cards))
    if len(matches):
        for match in matches:
            e = embed_card(match)
            await ctx.send(embed=e)
    else:
        await ctx.send('No matches')

@bot.event
async def on_message(message):
    if 'hastur' in message.content.lower():
        await message.channel.send(message.author.name + ' takes 1 horror')
    await bot.process_commands(message)
    
get_cards()
bot.run(token)