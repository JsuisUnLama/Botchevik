# Libraries
import re

from discord.ext import commands
from discord import Embed
from discord import Colour
from utils import errormanager as em
from config.public import ERROR_MESSAGE_LIFETIME, LEWD_USE_API, USER_AGENT
from bs4 import BeautifulSoup
import aiohttp

import logging
log = logging.getLogger(__name__)

# Class
class Lewd(commands.Cog):

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
        self.http_session   = aiohttp.ClientSession(loop=self.bot.loop, headers={'User-agent': USER_AGENT})
        error_msg_for_users = em.standardized_error("Weird thing happened when I reached the 'site'. Please try back in a few minutes")

        async with self.http_session.get('https://nhentai.net/random/', allow_redirects=False) as r:
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

            if LEWD_USE_API:
                res = await self.retrieve_tags_by_api(dj_id)
            else:
                res = await self.retrieve_tags_by_web_scrapping(dj_id)

            if res is False:
                await ctx.send(error_msg_for_users, delete_after=ERROR_MESSAGE_LIFETIME)
                return


            embed = Embed(color=Colour.dark_purple(), title="✨ **Sauce**")
            embed.add_field(name="ID", value=dj_id)
            embed.add_field(name="Tags", value="`"+'`\n`'.join(res)+"`", inline=False)

            await ctx.send(embed=embed)

        await self.http_session.close()


    async def retrieve_tags_by_api(self,id_gal):
        async with self.http_session.get('https://nhentai.net/api/gallery/{id}'.format(id=id_gal)) as r_gal:
            if r_gal.status != 200:
                log.error("API : Couldn't retrieve the gallery with the ID ({}), got status code {}".format(id_gal, r_gal.status))
                return False

            try:
                data = await r_gal.json()
            except Exception as e:
                log.error("API : Got error while parsing gallery response : " + str(e))
                return False

            if 'tags' not in data:
                log.error("API : Couldn't retrieve the gallery tags with the ID ({}), happened after json parsing".format(id_gal))
                return False


            return [tag['name'] for tag in data['tags']]


    async def retrieve_tags_by_web_scrapping(self, id_gal):
        async with self.http_session.get('https://nhentai.net/g/{id}'.format(id=id_gal)) as r_gal:
            if r_gal.status != 200:
                log.error("Web Scrapper : Couldn't retrieve the gallery with the ID ({}), got status code {}".format(id_gal, r_gal.status))
                return False

            data = await r_gal.read()
            soup = BeautifulSoup(data, features="html.parser")

            tags = soup.select("#tags div.tag-container:nth-child(3) a")

            if tags is None:
                log.error("Web scrapper : Couldn't retrieve the tag in the gallery page")
                return False

            return [tag.find(text=True) for tag in tags]



# Setup
def setup(bot):
    bot.add_cog(Lewd(bot))