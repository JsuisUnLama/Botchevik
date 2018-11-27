# Command: pf
# Arguments: [type | int]
# Description: post a pikachu face [of insanity level [int] or of type [type]]
# Author: @JsuisUnLama

# Libraries
import logging
import sqlite3
import discord
import os.path
from discord.ext import commands
from io import BytesIO
from discord import Embed
from discord import Colour
from config.public import DATABASE_NAME
from config.public import MIN_INSANITY_LEVEL
from config.public import MAX_INSANITY_LEVEL

# Create logger
log = logging.getLogger(__name__)

# Class
class PikachuFace:

    # Init
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pf', 
                      aliases=['pikachu','pikachuface','surprisedpikachu'],
                      brief='react with a surprised pikachu face',
                      description="display a surprised pikachu face of intensity [int] or of type [type]",
                      usage="[int | type]")
    async def pf_retrieve(self, ctx, attr = "0"):

        # Connection to the database
        conn = sqlite3.connect(DATABASE_NAME)
        
        # Managing help argument
        if attr == "help":
            cursor = conn.cursor()
            cursor.execute("SELECT name_pika FROM pikachus")
            response = cursor.fetchall()
            arglist = [n[0] for n in response]

            embed = Embed(color=Colour.gold(), title="😮 **Possible Arguments**")
            embed.add_field(name="Number", value= str(MIN_INSANITY_LEVEL) + " up to " + str(MAX_INSANITY_LEVEL))
            embed.add_field(name="Type", value="`"+'`\n`'.join(arglist[MAX_INSANITY_LEVEL+1:])+"`", inline=False)

            await ctx.send(embed=embed)

        # Managing command
        else:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT image_pika FROM pikachus WHERE name_pika=?", (attr,))
                response = cursor.fetchone()
                if(response is None):
                    await ctx.send('⚠ **Error:** couldn\'t fetch any pikachu (argument ' + attr + ' not recognized) ⚠\n              You can find the possible arguments by writing `-pf help`')
                else:
                    response = response[0]
                    img = BytesIO(open(os.path.join("res", "pikachuface", response), 'rb').read())
                    await ctx.message.delete()
                    await ctx.send(file = discord.File(img.getvalue(), 'dummy.png'))
            except sqlite3.OperationalError as e:
                log.error("Command has failed : " + str(e))
            finally:
                conn.close()

# Setup
def setup(bot):
    bot.add_cog(PikachuFace(bot))