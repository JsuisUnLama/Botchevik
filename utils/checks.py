from discord import TextChannel
from discord.ext import commands

#
# Contains all the checks function used in this bot
# Checks : https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#checks
#

def is_nsfw_or_dm():
    def pred(ctx):
        if isinstance(ctx.channel, TextChannel):
            return ctx.channel.is_nsfw()
        return True  # DMChannel or GroupChannel

    return commands.check(pred)