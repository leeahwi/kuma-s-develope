import discord
import asyncio
import youtube_dl
import requests
import re
import openpyxl
import os

from features import *
from settings import *

client = discord.Client()


BOTID = os.environ['BOT_USER_ID']
OWNERID = os.environ['SERVER_OWNER_USER_ID']
COMMANDPREFIX = '>'


@client.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))
    print('Invite URL: ' + 'https://discordapp.com/oauth2/authorize?&client_id=' + client.user.id + '&scope=bot&permissions=0')
	
# Announce the change in voice state through text to speech (ignores mutes/deafens)
@client.event
async def on_voice_state_update(before, after):
    # Ensure bot is connected to voice client (!join has been used)
    if client.is_voice_connected(before.server) == True:
        global player #모든 유저에 해당하는 구절인가?
        previousChannel = before.voice_channel
        newChannel = after.voice_channel

        # Bot only talks when user's channel changes, not on mutes/deafens
        if previousChannel != newChannel:
            # When user joins or moves to bot's channel 유저가 봇이 있는 채널에서 나가거나 들어올때
            if newChannel == currentChannel:
                tts.createAnnouncement(after.name, '이(가) 들어왔어요')
		#features/tts.py
            # When user leaves bot's channel
            elif previousChannel != None and newChannel == None and previousChannel == currentChannel:
                tts.createAnnouncement(after.name, '이(가) 나갔어요')
		
            # When user moves out of bot's channel to a new channel
            elif previousChannel == currentChannel and newChannel != currentChannel:
                tts.createAnnouncement(after.name, '이(가) 다른 채널로 이동했어요')

            # After user joins, leaves or moves, announce the new announcement
            if (newChannel == currentChannel or previousChannel != None and
                newChannel == None and previousChannel == currentChannel or
                previousChannel == currentChannel and newChannel != currentChannel):

                try:
                    if player.is_playing() == False:
                        player = voice.create_ffmpeg_player('announce.mp3')
                        player.start()

                except NameError:
                    player = voice.create_ffmpeg_player('announce.mp3')
                    player.start()

			
@client.event
async def on_message(message):
    # If the message author isn't the bot and the message starts with the
    # command prefix ('!' by default), check if command was executed
    if message.author.id != BOTID and message.content.startswith(COMMANDPREFIX):
	# 봇의 메세지가 명령으로 인식 안되게 함
        # Remove prefix and change to lowercase so commands aren't case-sensitive
        message.content = message.content[1:].lower()
          #conmmandprefix 다음 내용을 message.content로 받음
        # Shuts the bot down - only usable by the bot owner specified in config
        if message.content.startswith('shutdown') and message.author.id == OWNERID:
            await client.send_message(message.channel, '전 이제 잘게요~ 쿰나잇')
            await client.logout()
            await client.close()

        # Allows owner to set the game status of the bot
        elif message.content.startswith('status') and message.author.id == OWNERID:
            await client.change_presence(game=discord.Game(name=message.content[7:]))
	#ex)!status with discord studing > discord studing으로 봇 상태 변경
	
	 # Help Message, sends a personal message with a list of all the commands
        # and how to use them correctly
        elif message.content.startswith('help'):
            await client.send_message(message.channel, '1대1로 사용 명령어 보낼게요!(아직 안되는 기능 많아요..)')
            await client.send_message(message.author, helpMessage.helpMessage)
	#예시 !help 명령어 입력한 유저에게 features/helpmessage 내용 전달
	
      # Searches the second word following pythonhelp in python docs
        elif message.content.startswith('pythonhelp'):
            messagetext = message.content
            split = messagetext.split(' ')
            if len(split) > 1:
                messagetext = split[1]
                await client.send_message(message.channel, 'https://docs.python.org/3/search.html?q=' + messagetext)
		#pythonhelp 도움말 보냄
		
	  # Random cat gif
        elif message.content.startswith('catgif'):
            await client.send_message(message.channel, cats.getCatGif())
	# Random cat picture
        elif message.content.startswith('cat'):
            await client.send_message(message.channel, cats.getCatPicture())
	#features/cats.py
	
 ########## VOICE COMMANDS ##########

        # Will join the voice channel of the message author if they're in a channel
        # and the bot is not currently connected to a voice channel
        elif message.content.startswith('join'):
            if message.author.voice_channel != None and client.is_voice_connected(message.server) != True:
                global currentChannel
                global player
                global voice
                currentChannel = client.get_channel(message.author.voice_channel.id)
                voice = await client.join_voice_channel(currentChannel)

            elif message.author.voice_channel == None:
                await client.send_message(message.channel, '절 부른 사람이 음성채널에 없어요..')

            else:
                await client.send_message(message.channel, '이미 들왔어!')
		
	# Will leave the current voice channel
        elif message.content.startswith('leave'):
            if client.is_voice_connected(message.server):
                currentChannel = client.voice_client_in(message.server)
                await currentChannel.disconnect()
		
		
   # Will play music using the following words as search parameters or use the
        # linked video if a link is provided
        elif message.content.startswith('play'):
            if message.author.voice_channel != None:
		#유저가 음성채널에 들어가 있는경우
                if client.is_voice_connected(message.server) == True:
			#음성 연결 완료시
                    try:
                        if player.is_playing() == False:
                            print('추가...중...')
                            player = await voice.create_ytdl_player(youtubeLink.getYoutubeLink(message.content))
                            player.start()
                            await client.send_message(message.channel, ':musical_note: Currently Playing: ' + player.title)

                        else:
                            print('is playing')

                    except NameError:
                        print('name error')
                        player = await voice.create_ytdl_player(youtubeLink.getYoutubeLink(message.content))
                        player.start()
                        await client.send_message(message.channel, ':musical_note: Currently Playing: ' + player.title)

                else:
                    await client.send_message(message.channel, '!join 치면 되(돼?)')

            else:
                await client.send_message(message.channel, 'You are not connected to a voice channel. Enter a voice channel and use !join first.')

        # Will pause the audio player
        elif message.content.startswith('pause'):
            try:
                player.pause()

            except NameError:
                await client.send_message(message.channel, 'Not currently playing audio.')

        # Will resume the audio player
        elif message.content.startswith('resume'):
            try:
                player.resume()

            except NameError:
                await client.send_message(message.channel, 'Not currently playing audio.')

        # Will stop the audio player
        elif message.content.startswith('stop'):
            try:
                player.stop()

            except NameError:
                await client.send_message(message.channel, 'Not currently playing audio.')
		
TOKEN = os.environ['BOT_TOKEN']
client.run(TOKEN)
