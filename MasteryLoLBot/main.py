
import asyncio
import random

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='M?', description='Testing for MQP!', intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
@bot.command()
async def changePref(ctx, pref: str):
    bot.command_prefix = pref
    await ctx.send('Succesfully updated prefix to ' + pref)
@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")
bot.run('INSERT BOT TOKEN HERE')