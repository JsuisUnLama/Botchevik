# Libraries
import re

import requests
from discord.ext import commands
from discord import Embed
from discord import Colour
from config.public import USER_AGENT

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
        headers = {'User-Agent': USER_AGENT}
        r = requests.get('https://nhentai.net/random/', allow_redirects=False, headers=headers)

        m = re.search(r'/g/(\d{1,6})/', r.headers['Location'])

        if not m:
            print("Couldn't retrieve id")

        dj_id = m.group(1)
        r     = requests.get('https://nhentai.net/api/gallery/{id}'.format(id=dj_id))
        data  = r.json()

        if 'tags' not in data:
            print("Couldn't retrieve tags")

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