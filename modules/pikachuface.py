# Command: pf
# Arguments: [type | int]
# Description: post a pikachu face [of insanity level [int] or of type [type]]
# Author: @JsuisUnLama

# Libraries
from discord.ext import commands
from discord import File
from io import BytesIO
import sqlite3
import discord
import os.path

class PikachuFace:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pf', pass_context=True)
    async def pf_retrieve(self, ctx, attr = "0"):
        conn = sqlite3.connect('botchevik.db')
        try:
            cursor = conn.cursor()
            name = "pf_" + ("il" if attr.isdigit() else "") + attr
            cursor.execute("SELECT image_pika FROM pikachus WHERE name_pika=?", (name,))
            response = cursor.fetchone()
            if(response is None):
                await ctx.send('⚠ **Error:** couldn\'t fetch any pikachu (' + attr + ' not recognized) ⚠')
            else:
                response = response[0]
                img = BytesIO(open(os.path.join("res", "pikachuface", response), 'rb').read())
                await ctx.message.delete()
                await ctx.send(file = discord.File(img.getvalue(), 'dummy.png'))
        except sqlite3.OperationalError as e:
            print(e)
        finally:
            conn.close()

def setup(bot):
    bot.add_cog(PikachuFace(bot))