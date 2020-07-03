import discord
import requests
from discord.ext import commands
from discord import Embed
import random
import json

api = 'https://api.covid19api.com/'

with open('config.json', 'r') as f:  # load bot config
    data = json.load(f)
    token = data["token"]
    prefix = data['prefix']
    description = data['description']

bot = commands.Bot(command_prefix=prefix, description=description)


@bot.event
async def on_ready():
    print(f'[BOT] {bot.user.name} running...')


@bot.command()
async def stats(ctx, *args):
    """Sends the coronavirus status for a single country or the world"""
    if len(args) == 0:  # if no args, show global stats
        r = requests.get(url=api + 'summary')
        rdict = json.loads(r.text)
        response = rdict['Global']
        date = rdict['Date']
        embed = Embed(title="Global Coronavirus Statistics", color=0x00FF00)
        for key in response:
            embed.add_field(name=key, value=response[key])
        embed.add_field(name='Date', value=date)
        await ctx.send(embed=embed)
    else:  # if args, find country stats
        country = args[0]
        for i in args[1:]:  # args to string for if country name is more than one word
            country += ' ' + i
        r = requests.get(url=api + 'summary')
        rdict = json.loads(r.text)
        response = rdict['Countries']
        countrieslist = ""
        countrystats = {}
        for i in response:  #  loop through API response to find correct country
            countrieslist += '\n' + i['Country'].lower()
            if i['Country'].lower() == country:
                countrystats = i
        try:
            embed = Embed(
                title=f"{countrystats['Country']}'s Coronavirus Statistics", color=0x00FF00)
            for key in countrystats:
                embed.add_field(name=key, value=countrystats[key])
            await ctx.send(embed=embed)
        except Exception:  # if any errors, show error embed
            embed = Embed(title="ERROR", color=0xFF0000)
            embed.add_field(
                name='API ERROR', value='Country could not be found, here is a full list:')
            # discord has a max embed text
            embed.add_field(name='Countries List 1',
                            value=countrieslist[:1024])
            # length of 1024 so just cut it in half
            embed.add_field(name='Countries List 2',
                            value=countrieslist[1024:])
            await ctx.send(embed=embed)

bot.run(token)
