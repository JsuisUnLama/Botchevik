# Libraries
import re
import sqlite3
import discord
import requests
import logging
import asyncio
import os.path
from random import randint
from discord.ext import commands
from discord import Embed
from discord import Colour
from config.public import ERROR_MESSAGE_LIFETIME
from config.public import HELP_MESSAGE_LIFETIME
from config.public import DATABASE_NAME
from config.public import USER_AGENT
from utils import errormanager as em
from utils import supportedservices as ss
from utils import youtubedlsource as ys

# Create logger
log = logging.getLogger(__name__)

# Loading opus
if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

# On error
async def on_error(self, event, vc, db):
    await vc.disconnect()
    db.close()

# Class
class AudioMeme:

    # Init
    def __init__(self, bot):
        self.bot = bot
        self.is_itts = False

    # Command addmeme declaration
    @commands.command(name='addmeme', 
                      aliases=['memeadd','addm'],
                      brief='add a meme for the bot to display',
                      description="add meme <meme_name> refering to <link> to the database. Both name and link shall be unique",
                      usage=" <meme_name (which musn't be 'help')> <link (must be youtube or mp3)>")
    async def addmeme(self, ctx, name="help", link="help"):

        # Connection to the database
        db = sqlite3.connect(DATABASE_NAME)

        # Checking number of arguments
        if name == "help" or link == "help":
            logMsg = "addmeme command didn't met the requirements to fire arguments wise"
            errMsg = "You didn't provide enough argument (or the special one a.k.a. 'help')"
            additionalInfo = 'Usage: `' + ctx.command.name + ctx.command.usage + '`'
            log.warning(logMsg)
            await ctx.send(em.standardized_error(errMsg,additionalInfo),delete_after=ERROR_MESSAGE_LIFETIME)
            return

        # Is the name and link unique ?
        try:
            cursor = db.cursor()
            cursor.execute("SELECT name_meme FROM memes WHERE name_meme = ?", (name,))
            response = cursor.fetchone()

            if response is not None:
                logMsg = "Attempt to add something to the database has failed for it already existed and was unique name wise"
                errMsg = "`" + name + "` is already referenced in the database"
                additionalInfo = 'You can find the already taken names by writing `-meme help`'
                log.warning(logMsg)
                await ctx.send(em.standardized_error(errMsg,additionalInfo),delete_after=ERROR_MESSAGE_LIFETIME)
                return

            cursor.execute("SELECT link_meme FROM memes WHERE link_meme = ?", (link,))
            response = cursor.fetchone()
            if response is not None:
                cursor.execute("SELECT name_meme FROM memes WHERE link_meme = ?", (link,))
                response = cursor.fetchone()
                logMsg = "Attempt to add something to the database has failed for it already existed and was unique link wise"
                errMsg = "This provided link is already referenced in the database as the result of `-meme " + response[0] + "`"
                additionalInfo = 'You can find the already taken names by writing `-meme help`'
                log.warning(logMsg)
                await ctx.send(em.standardized_error(errMsg,additionalInfo),delete_after=ERROR_MESSAGE_LIFETIME)
                return
                
            # Does the link exist ?
            try:
                headers = {'User-Agent': USER_AGENT}
                r = requests.get(link, allow_redirects=False, headers=headers)
            except Exception as e:
                logMsg = "Request error: " + str(e)
                errMsg = "This provided link doesn't seem to refer to anything"
                log.error(logMsg)
                await ctx.send(em.standardized_error(errMsg),delete_after=ERROR_MESSAGE_LIFETIME)
                return

            # Does it have a supported Content-Type ?
            accepted = ['audio/mpeg','video/mpeg','video/mp4','video/webm','application/ogg']
            ctype = r.headers['Content-Type']
            serv = ss.is_from_a_supported_service(self,link)

            if serv is '' and ctype not in accepted:
                logMsg = "Provided link doesn't have supported Content-Type nor is from a supported service"
                errMsg = "The provided link isn't supported"
                log.error(logMsg)
                await ctx.send(em.standardized_error(errMsg),delete_after=ERROR_MESSAGE_LIFETIME)
                return

            # Add meme
            try:
                is_special = 1 if serv is not '' else 0
                cursor.execute("INSERT INTO memes(name_meme,link_meme,is_special) VALUES(?,?,?)", (name,link,is_special,))
                db.commit()
            except Exception as e:
                logMsg = "Database error: " + str(e)
                errMsg = "Failed to add the meme in the database"
                log.error(logMsg)
                await ctx.send(em.standardized_error(errMsg),delete_after=ERROR_MESSAGE_LIFETIME)
                return

            await ctx.message.delete()
            await ctx.send("`" + name + "` meme successfuly added !")
                
        except sqlite3.OperationalError as e:
            logMsg = "Command has failed : " + str(e)
            log.error(logMsg)
        finally:
            db.close()



    # Command delmeme declaration
    @commands.command(name='delmeme', 
                      aliases=['memedel','delm'],
                      brief='delete a meme for the bot to display',
                      description="delete meme <meme_name> from the database. Only for those higher than the bot in the hierarchy",
                      usage="<meme_name>")
    async def delmeme(self, ctx, name="help"):

        # Connection to the database
        db = sqlite3.connect(DATABASE_NAME)

        # Managing help argument
        if name in ['help','h']:
            try:
                cursor = db.cursor()
                cursor.execute("SELECT name_meme FROM memes")
                response = cursor.fetchall()
                arglist = [n[0] for n in response]

                roles = ctx.guild.roles
                roles_id = [role.id for role in roles]
                split_index = roles_id.index(ctx.guild.me.top_role.id)
                high_enough_roles_id = roles_id[split_index+1:]
                high_enough_roles = [ctx.guild.get_role(heri).name for heri in high_enough_roles_id]

                specials = ['`obliterate them all`','`help` / `h`']

                embed = Embed(color=Colour.darker_grey(), title="☠ **Possible Arguments**")
                embed.add_field(name="Special", value=""+'\n'.join(specials)+"", inline=False)
                embed.add_field(name="People allowed to delete", value="`"+'`\n`'.join(high_enough_roles)+"`", inline=False)
                if not arglist:
                    embed.add_field(name="Name", value="The database is completely empty, try adding some memes first", inline=False)
                else:
                    embed.add_field(name="Name", value="`"+'`\n`'.join(arglist)+"`", inline=False)

                await ctx.send(embed=embed,delete_after=HELP_MESSAGE_LIFETIME)

            except sqlite3.OperationalError as e:
                logMsg = "Command has failed : " + str(e)
                log.error(logMsg)
                return

        else:
            # Are you high enough in the hierarchy ?
            if ctx.author.top_role < ctx.guild.me.top_role:
                logMsg = "An unworthy Member tried to delete the meme '" + name + "'"
                errMsg = "You are not allowed to delete a meme from the database"
                log.warning(logMsg)
                await ctx.send(em.standardized_error(errMsg),delete_after=ERROR_MESSAGE_LIFETIME)
                return

            # Connection to the database
            db = sqlite3.connect(DATABASE_NAME)

            # Does <name> refer to something in the database ?
            try:
                cursor = db.cursor()
                if name != "obliterate them all":
                    cursor.execute("SELECT id_meme FROM memes WHERE name_meme = ?", (name,))
                    id_meme = cursor.fetchone()

                    if id_meme is None:
                        logMsg = "Attemp to target something that doesn't exist in the database"
                        errMsg = name + " doesn't seem to refer to anything in the database" 
                        additionalInfo = "You can find existing memes and this command options by writing `-delmeme help`"
                        log.error(logMsg)
                        await ctx.send(em.standardized_error(errMsg,additionalInfo),delete_after=ERROR_MESSAGE_LIFETIME)
                        return

                else:
                    cursor.execute("SELECT id_meme FROM memes")
                    id_memes = cursor.fetchall()
                    
                    if not id_memes:
                        logMsg = "Attemp to target objects in an empty database"
                        errMsg = "Database is empty... YEET"
                        additionalInfo = "You can find existing memes and this command options by writing `-delmeme help`"
                        log.error(logMsg)
                        await ctx.send(em.standardized_error(errMsg,additionalInfo),delete_after=ERROR_MESSAGE_LIFETIME)
                        return

                # Delete meme
                try:
                    if name == 'obliterate them all':
                        cursor.execute("DELETE FROM memes")
                    else:
                        cursor.execute("DELETE FROM memes WHERE id_meme = ?", (id_meme[0],))

                    db.commit()

                except Exception as e:
                    logMsg = "Database error: " + str(e)
                    errMsg = "Failed to delete the meme(s) from the database"
                    log.error(logMsg)
                    await ctx.send(em.standardized_error(errMsg),delete_after=ERROR_MESSAGE_LIFETIME)
                    return
                    
                await ctx.message.delete()
                if name == "obliterate them all":
                    await ctx.send("You madman successfuly destroyed all the memes you had in your database. Psycho.")
                else:
                    await ctx.send("`" + name + "` meme successfuly deleted !")

            except sqlite3.OperationalError as e:
                logMsg = "Command has failed : " + str(e)
                log.error(logMsg)
            finally:
                db.close()



    # Command meme declaration
    @commands.command(name='meme', 
                      aliases=['m'],
                      brief='display a given meme',
                      description="display the audio meme <meme_name> recognized in the database",
                      usage="<meme_name>")
    async def meme(self, ctx, name="h"):

        # Connection to the database
        db = sqlite3.connect(DATABASE_NAME)

        # Managing help argument
        if name in ['help','h']:
            try:
                cursor = db.cursor()
                cursor.execute("SELECT name_meme FROM memes")
                response = cursor.fetchall()
                arglist = [n[0] for n in response]

                specials = ['`random` / `r`','`help` / `h`']
                embed = Embed(color=Colour.dark_green(), title="🎨 **Possible Arguments**")
                embed.add_field(name="Special", value=""+'\n'.join(specials)+"", inline=False)
                if not arglist:
                    embed.add_field(name="Name", value="The database is completely empty, try adding some memes first", inline=False)
                else:
                    embed.add_field(name="Name", value="`"+'`\n`'.join(arglist)+"`", inline=False)

                await ctx.send(embed=embed,delete_after = HELP_MESSAGE_LIFETIME)

            except sqlite3.OperationalError as e:
                logMsg = "Command has failed : " + str(e)
                log.error(logMsg)
                return
        else:

            # Is the author connected in a vocal channel which is not afk ?
            vs = ctx.author.voice
            if vs is None or vs.afk:
                logMsg = "Member tried to trigger audio meme without being in any supported voice channel"
                errMsg = "You have to be in a voice chat, and it shouldn't be the AFK one"
                log.error(logMsg)
                await ctx.send(em.standardized_error(errMsg),delete_after=ERROR_MESSAGE_LIFETIME)
                return
            
            # Is the bot already connected to a channel (and thus doing something else) ?
            if len(self.bot.voice_clients) is not 0:
                logMsg = "Bot is already in use"
                errMsg = "Bot is already in use"
                log.error(logMsg)
                await ctx.send(em.standardized_error(errMsg),delete_after=ERROR_MESSAGE_LIFETIME)
                return

            # Is there at least one meme in the database ?
            try:
                cursor = db.cursor()
                cursor.execute("SELECT id_meme FROM memes")
                memes_nb = cursor.fetchall()
                if not memes_nb:
                    logMsg = "-meme command was done while there was no memes in the database"
                    errMsg = "There are currently no memes in the database"
                    additionalInfo = "You can add memes to the database by writing `-addmeme <name> <link>`"
                    log.warning(logMsg)
                    await ctx.send(em.standardized_error(errMsg,additionalInfo),delete_after=ERROR_MESSAGE_LIFETIME)
                    return
                
                # Random option. If not, does <name> refer to something in the database ?    
                if name in ['random','r']:
                    cursor.execute("SELECT link_meme from memes")
                    response_list = cursor.fetchall()
                    index = randint(0,len(response_list)-1)
                    response = response_list[index] 
                else:
                    cursor.execute("SELECT link_meme FROM memes WHERE name_meme = ?", (name,))
                    response = cursor.fetchone()
                    if response is None:
                        logMsg = "Attemp to fetch something that doesn't exist in the database"
                        errMsg = name + " doesn't seem to refer to anything"
                        additionalInfo = "You can find the existing memes by writing `-meme help`"
                        log.warning(logMsg)
                        await ctx.send(em.standardized_error(errMsg,additionalInfo),delete_after=ERROR_MESSAGE_LIFETIME)
                        return
                link = response[0]
                
                # Can the bot join your channel ?
                try:
                    vc = await vs.channel.connect(timeout=1.0, reconnect=False)
                except Exception as e:
                    logMsg = "Bot has failed to join voice channel: " + str(e)
                    errMsg = "Bot has failed to join voice channel"
                    log.error(logMsg)
                    await ctx.send(em.standardized_error(errMsg),delete_after=ERROR_MESSAGE_LIFETIME)
                    return

                # Trigger meme
                await ctx.message.delete()
                cursor.execute("SELECT is_special FROM memes WHERE link_meme = ?", (link,))
                is_special = cursor.fetchone()
                if is_special[0] == 1:
                    meme = await ys.YTDLSource.from_url(link)
                else:
                    meme = discord.FFmpegPCMAudio(link)
                
                vc.play(meme)
                self.bot.loop.create_task(self.wait_meme_completion(ctx))
                return
            
            except sqlite3.OperationalError as e:
                logMsg = "Command has failed : " + str(e)
                log.error(logMsg)
            finally:
                db.close()



    # Command itts declaration
    @commands.command(name='itts', 
                      aliases=['quitm','stopm'],
                      brief='stop the display of a meme',
                      description="provided the bot is displaying a meme in a vocal channel, disconnect it",
                      usage="")
    async def itts(self, ctx):
        self.is_itts = True
        await ctx.message.delete()
        vc = ctx.voice_client
        
        if vc is not None:
            await vc.disconnect()



    # Wait until completion
    async def wait_meme_completion(self, ctx):
        vc = ctx.voice_client
        if self.is_itts: # Will work in v2 I swear 
            vc.play(discord.FFmpegPCMAudio(os.path.join('res', 'memes', 'itts.mp3')))
            self.bot.loop.create_task(self.wait_meme_completion(ctx))
        else:
            while vc.is_playing():
                await asyncio.sleep(1)
        
        await vc.disconnect()



# Setup
def setup(bot):
    bot.add_cog(AudioMeme(bot))