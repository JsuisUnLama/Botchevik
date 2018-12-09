# Libraries
import re

from discord.ext import commands
from discord import Embed
from discord import Colour
from utils import http, errormanager as em
from config.public import ERROR_MESSAGE_LIFETIME
import logging

log = logging.getLogger(__name__)

# Class
class Lewd:

    # Init
    def __init__(self, bot):
        self.bot = bot

    # Command sauce? declaration
    @commands.command(name='sauce?', 
                      aliases=['sauce','s?','nh'],
                      brief='When you want a random number  ( ͡° ͜ʖ ͡°)',
                      description="Bring you a random doujin's ID while unveiling its tags",
                      usage="")
    async def sauce(self, ctx):
        r = await http.request('https://nhentai.net/random/', allow_redirects=False)
        error_msg_for_users = em.standardized_error("Weird thing happened when I reached the 'site'. Please try back in a few minutes")

        if r.status != 302:
            log.error("Couldn't reach nhentai, got status code {}".format(r.status))
            await ctx.send(error_msg_for_users, delete_after=ERROR_MESSAGE_LIFETIME)
            return

        m = re.search(r'/g/(\d{1,6})/', r.headers['Location'])

        if not m:
            log.error("Couldn't retrieve the ID from the random route")
            await ctx.send(error_msg_for_users, delete_after=ERROR_MESSAGE_LIFETIME)
            return

        dj_id = m.group(1)
        r_gal = await http.request('https://nhentai.net/api/gallery/{id}'.format(id=dj_id))

        if r_gal.status is not 200:
            log.error("Couldn't retrieve the gallery with the ID ({}), got status code {}".format(dj_id, r_gal.status))
            await ctx.send(error_msg_for_users, delete_after=ERROR_MESSAGE_LIFETIME)
            return

        try :
            data  = await r_gal.json()
        except Exception as e:
            log.error("Got error while parsing gallery response : " + str(e))
            await ctx.send(error_msg_for_users, delete_after=ERROR_MESSAGE_LIFETIME)
            return

        if 'tags' not in data:
            log.error("Couldn't retrieve the gallery tags with the ID ({}), happened after json parsing".format(dj_id))
            await ctx.send(error_msg_for_users, delete_after=ERROR_MESSAGE_LIFETIME)
            return

        tags_list = []

        for tag in data['tags']:
            tags_list.append(tag['name'])

        embed = Embed(color=Colour.dark_purple(), title="✨ **Sauce**")
        embed.add_field(name="ID", value=dj_id)
        embed.add_field(name="Tags", value="`"+'`\n`'.join(tags_list)+"`", inline=False)

        await ctx.send(embed=embed)

# Setup
def setup(bot):
    bot.add_cog(Lewd(bot))