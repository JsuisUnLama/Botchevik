from discord.ext import commands
from discord import Embed, Color
import logging
from config.public import ERROR_MESSAGE_LIFETIME
from utils import errormanager as em

log = logging.getLogger(__name__)

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sharemusic',
                      aliases=['buymymixtape','spotifyshare', 'sm', 'ms'],
                      brief="Share the spotify track that you're currently listening to",
                      description="Post a spotify link of the music track you're currently listening to",
                      usage="")
    @commands.guild_only()
    async def share(self, ctx):
        spotify_info = None
        for activity in ctx.author.activities:
            if str(activity) is "Spotify":
                spotify_info = activity
                break

        if not spotify_info:
            embed = Embed(description="You're not listening to music on Spotify ! (or Discord doesn't recognize it)", color=Color.red())
            await ctx.send(embed=embed, delete_after=ERROR_MESSAGE_LIFETIME)
            return

        embed = Embed(title="Music sharing", description="Track shared by <@{}>".format(ctx.author.id), color=spotify_info.color)
        embed.add_field(name="Artist(s)", value=spotify_info.artist)
        embed.add_field(name="Title", value=spotify_info.title)
        embed.set_thumbnail(url=spotify_info.album_cover_url)
        async with ctx.channel.typing():
            await ctx.send(embed=embed)
            await ctx.send(content="https://open.spotify.com/track/{}".format(spotify_info.track_id))

    @share.error
    async def share_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(em.standardized_error("Can't run this command here (Needs to be in a guild)"),  delete_after=ERROR_MESSAGE_LIFETIME)
            log.info("The 'spotify.share' command has been run in the '{}' channel and has generated a checkfailure".format(ctx.channel))


def setup(bot):
    bot.add_cog(Spotify(bot))