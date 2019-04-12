from discord.ext import commands
import utils.errormanager as em
from config.public import ERROR_MESSAGE_LIFETIME
from discord import Embed
from discord import Colour

import re
import logging
log = logging.getLogger(__name__)

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stealemoji',
                      aliases=['steal','stealthis'],
                      brief='Give you the emoji in the message before the command',
                      description="List all the link to download the emoji in the message posted before the command",
                      usage="")
    async def steal_emoji(self, ctx):
        url            = "https://cdn.discordapp.com/emojis/{emoji_id}.{ext}"
        regex          = r"<(a)?:[^:]*:(\d*)>"
        message_before = (await ctx.channel.history(limit=1, before=ctx.message).flatten())[0]

        m = re.findall(regex, message_before.content)

        if not m:
            err_msg = em.standardized_error("No emote found in the previous message")
            await ctx.send(err_msg, delete_after=ERROR_MESSAGE_LIFETIME)
            return

        url_found = []
        for match in m:
            data = {
                "emoji_id" : match[1],
                "ext" : ("gif" if match[0] == 'a' else "png")
            }
            url_found.append(url.format(**data))

        for url in url_found:
            embed = Embed(color=Colour.blurple(), title="🕵️ **Steal Emoji**")
            embed.add_field(name="Thief", value="<@{}>".format(ctx.author.id))
            embed.set_thumbnail(url=url)
            embed.add_field(name="Url", value=url)
            await ctx.send(embed=embed)






# Setup
def setup(bot):
    bot.add_cog(Miscellaneous(bot))