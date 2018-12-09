import youtube_dl
import discord
import asyncio
import functools
from config.public import MEME_BASE_VOLUME

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn -loglevel panic'
}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': './tmp/%(extractor)s-%(id)s-%(title)s.%(ext)s', # PATH A CHANGER
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume):
        self.source = source
        super().__init__(self.source, volume)
        self.data = data
        self.title = data.get('title')
        self.uploader = data.get("uploader")
        self.uploader_url = data.get("uploader_url")
        self.url = data.get('url')
        self.duration = data.get("duration")
        self.host = data.get("extractor_key")
        self.webpage_url = data.get('webpage_url')
        self.thumbnail_url = data.get("thumbnail", "")

    @classmethod
    async def from_url(self, url, *, loop=None, stream=False, volume=MEME_BASE_VOLUME):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist. This shouldn't need to happen but in case it does.
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return self(discord.FFmpegPCMAudio(filename, options=ffmpeg_options), data=data, volume=volume)
