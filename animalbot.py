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
    await bot.change_presence(game=discord.Game(name='공부중', type=1))

@bot.event
async def on_message(message):
    if message.content.startswith("!안녕"):
        await bot.send_message(message.channel, "안녕하세요")


access_token = os.environ['BOT_TOKEN']
bot.run(access_token)
