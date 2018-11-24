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
from config.public import DATABASE_NAME
from io import BytesIO

# Create logger
log = logging.getLogger(__name__)

# Class
class PikachuFace:

    # Init
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pf', description="A cute pikachu to react with :3")
    async def pf_retrieve(self, ctx, attr = "0"):

        # Connection to the database
        conn = sqlite3.connect(DATABASE_NAME)
        
        # Managing the command
        try:
            cursor = conn.cursor()
            name = "pf_" + ("il" if attr.isdigit() else "") + attr
            cursor.execute("SELECT image_pika FROM pikachus WHERE name_pika=?", (name,))
            response = cursor.fetchone()
            if(response is None):
                await ctx.send('⚠ **Error:** couldn\'t fetch any pikachu (argument ' + attr + ' not recognized) ⚠')
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