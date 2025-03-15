import discord
from discord.ext import commands
import yt_dlp
import asyncio

intents = discord.Intents.default()
intents.message_content = True

FFMPEG_OPTIONS = {'options' : '-vn'}
YDL_OPTIONS = {'format' : 'bestaudio' , 'noplaylist' : True}
class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []

    @commands.command()
    async def play(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("Santir Chele Tui kono Voice Channel Nai, Gandu!!")
        if not ctx.voice.client:
            await voice_channel.connect()

        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url = info['url']
                title = info['title']
                self.queue.qppend((url, title))
                await ctx.send(f'Added to queue: **{title}**')
            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)

        async def play_next(self, ctx):
            if self.queue:
                url, title = self.queue.pop(0)
                source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
                ctx.voice_client.play(source, after=lambda _:self.client.loop.create_task(self.play_next(ctx)))
                await ctx.send(f'Now playing **{title}**')
            elif not ctx.voice_client.is_playing():
                await ctx.send("Khankir chele Queue ta empty! Gaan de lawra!!")

        @commands.command()
        async def skip(self, ctx):
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send("Tu Pod Mara Ga")
                
client = commands.Bot(command_prefix='!', intents=intents)

async def main():
    await client.add_cog(MusicBot(client))
    await client.start('MTM0MDIzMTcwMDg1MjExMzQwOA.Ge9Rp-.87AzuP1Nwu_mEiC8nULXwfjv_0H8H2V5oTZE_E')

asyncio.run(main())    





