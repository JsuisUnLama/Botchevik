# Libraries
import logging
import sqlite3
import discord
import os.path
from discord.ext import commands
from io import BytesIO
from discord import Embed
from discord import Colour
from random import randint
from config.public import DATABASE_NAME
from config.public import ERROR_MESSAGE_LIFETIME
from utils import errormanager as em

# Create logger
log = logging.getLogger(__name__)

# Class
class PikachuFace:

    # Init
    def __init__(self, bot):
        self.bot = bot

    # Command pf declaration
    @commands.command(name='pf', 
                      aliases=['pikachu','pikachuface','spf'],
                      brief='react with a surprised pikachu face',
                      description="display a surprised pikachu face of intensity [int] or of type [type]",
                      usage="[int | type]")
    async def pf(self, ctx, attr = "0"):

        # Connection to the database
        db = sqlite3.connect(DATABASE_NAME)
        cursor = db.cursor()

        # Managing help argument
        if attr in ['help','h']:
            cursor.execute("SELECT name_pika FROM pikachus")
            response = cursor.fetchall()

            arglist = [n[0] for n in response]
            pika_type = arglist.copy()

            pika_il = []
            for arg in arglist:
                if arg.isdigit():
                    pika_il.append(int(arg)) 
                    pika_type.remove(arg)
            
            max_il = 0
            for il in pika_il:
                if il > max_il: 
                    max_il = il

            specials = ['`random` / `r`','`help` / `h`']

            embed = Embed(color=Colour.gold(), title="😮 **Possible Arguments**")
            embed.add_field(name="Special", value=""+'\n'.join(specials)+"", inline=False)
            embed.add_field(name="Insanity level", value= "`" + str(0) + "` up to `" + str(max_il) + "`", inline=False)
            embed.add_field(name="Type", value="`"+'`\n`'.join(pika_type)+"`", inline=False)

            await ctx.send(embed=embed)

        # Managing command 
        else:
            try:
                # Managing random argument
                if attr in ['random','r']:
                    cursor.execute("SELECT count(*) FROM pikachus")
                    pika_nb = cursor.fetchone()[0]
                    id_pika = randint(1,pika_nb)
                    cursor.execute("SELECT image_pika FROM pikachus WHERE id_pika = ?", (id_pika,))
                    response = cursor.fetchone()
                else:
                    cursor.execute("SELECT image_pika FROM pikachus WHERE name_pika=?", (attr,))
                    response = cursor.fetchone()

                    # Does the attribute refer to anything ?
                    if(response is None):
                        logMsg = "A user has failed to fetch a pikachu face from the database (arg was " + attr + ")"
                        errMsg = "Couldn't fetch any pikachu (argument **" + attr + "** not recognized)"
                        additionalInfo = "You can find the possible arguments by writing `-pf help`"
                        log.error(logMsg)
                        await ctx.send(em.standardized_error(errMsg,additionalInfo),delete_after=ERROR_MESSAGE_LIFETIME)
                        return
                
                # Display corresponding pikachu face
                img = BytesIO(open(os.path.join("res", "pikachuface", response[0]), 'rb').read())
                await ctx.message.delete()
                await ctx.send(file = discord.File(img.getvalue(), 'dummy.png'))

            except sqlite3.OperationalError as e:
                logMsg = "Command has failed : " + str(e)
                log.error(logMsg)
            finally:
                db.close()

# Setup
def setup(bot):
    bot.add_cog(PikachuFace(bot))