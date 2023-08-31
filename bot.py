import re

import discord
from discord.ext import commands
import bot_auth


# 봇 토큰
BOT_TOKEN = bot_auth.auth["token"]

# 정규 표현식을 사용하여 URL 추출
url_pattern = re.compile(r'\((.*?)\)')


# 원하는 intents 활성화
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 관련 이벤트 활성화
 
bot = commands.Bot(command_prefix='!', intents=intents)
 
@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
 
@bot.command()
async def hello(message):
    await message.channel.send('Hi!')

@bot.command()
async def history(ctx, limit: int = 100000):
    music_links = []
    file_path = 'music_links.txt'
    async for message in ctx.channel.history(limit=limit):
        if message.author.name == "노래하는하리보":
            song_url = None

            for embed in message.embeds:
                for field in embed.fields:
                    song_url = url_pattern.search(field.value)

            if song_url:
                music_links.append(song_url.group(1))
                print(song_url.group(1))

    with open(file_path, 'w') as file:
        for link in music_links:
            file.write(link + '\n')

bot.run(BOT_TOKEN)
