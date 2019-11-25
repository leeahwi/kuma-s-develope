import discord
import asyncio
import openpyxl
import os


bot = discord.Client()

@bot.event
async def on_ready():
    print("login")
    print(client.user.name)
    print(client.user.id)
    print("ㅡㅡㅡㅡㅡㅡ")
    game = discord.Game("군생활")
    await bot.change_presence(activity=game, status=None)

@bot.event
async def on_message(message):
 
    if message.author == client.user:
        return
 
    if message.content.startswith('hi'):
        await bot.send_message(message.channel, embed=discord.Embed(description="hi"))
        
access_token = os.environ['BOT_TOKEN']
bot.run(access_token)
