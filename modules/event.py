# Happen: whenever someone joins the server
# Task: send a private greeting message to him
# Author:

# Libraries
from discord import Embed, Colour
import logging
from discord.ext import commands

# Create logger
log = logging.getLogger(__name__)


# Class
class Event(commands.Cog):

    # Init
    def __init__(self, bot):
        self.bot = bot

    # Detecting new member
    @commands.Cog.listener()
    async def on_member_join(self, member):

        # Creating private channel discussion with member
        try:
            dm_channel = await member.create_dm()
        except Exception as e:
            print(e)
            log.warning("User " + member.name + " of id " + member.id + "could not receive the welcome message")
            return
        
        # Generating welcome message
        link = "https://roleypoly.com/s/" + str(member.guild.id)
        welcome_msg = "Hey 👋 Congrats for having joined **" + member.guild.name + "** !\n"
        welcome_msg += "Please 🙏 assign yourself some juicy roles here:\n"
        welcome_msg += link

        # Send welcome message
        await dm_channel.send(welcome_msg)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        if self.bot.user in msg.mentions:
            embed = Embed(
                color=Colour.red(),
                description="Oh, hey ! If you want to know all the commands I have, just type **" + self.bot.command_prefix + "help**"
            )
            await msg.channel.send(embed=embed)


# Setup
def setup(bot):
    bot.add_cog(Event(bot))
