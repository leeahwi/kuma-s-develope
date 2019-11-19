import discord
import asyncio
import openpyxl
import os


client = discord.Client()

@client.event
async def on_ready():
    print("login")
    print(client.user.name)
    print(client.user.id)
    print("ㅡㅡㅡㅡㅡㅡ")
    await client.change_presence(game=discord.Game(name='테스트 중', type=1))

@client.event
async def on_message(message):
    if message.content.startswith("!안녕"):
        await client.send_message(message.channel, "안녕하세요")


access_token = os.environ['BOT_TOKEN']
client.run(access_token)
