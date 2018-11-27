from discord.ext import commands
from config.public import MAX_NOT_ASSUMING_SECONDS
from config.public import MIN_NOT_ASSUMING_SECONDS
from config.public import MAX_NOT_ASSUMING_NEXT_SECONDS
import asyncio


class NotAssuming:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='na',
                      brief="Delete current message after x seconds",
                      description="Delete current message after x seconds",
                      usage="[seconds] The rest of your message")
    async def na(self, ctx, arg):
        if not arg.isdigit():
            return

        seconds = int(arg)

        if seconds == 0:
            seconds = MIN_NOT_ASSUMING_SECONDS

        if seconds > MAX_NOT_ASSUMING_SECONDS:
            seconds = MAX_NOT_ASSUMING_SECONDS

        await asyncio.sleep(seconds)
        await ctx.message.delete()

# class NotAssumingNext:
#
#   def __init__(self,bot):
#        self.bot = bot
#
#   @commands.command(name='nan',
#                     brief="Delete your next message after x seconds",
#                     description="Delete your next message after x seconds, provided you write it within the next " + MAX_NOT_ASSUMING_NEXT_SECONDS + " next seconds after this command",
#                     usage="[seconds]")

def setup(bot):
    bot.add_cog(NotAssuming(bot))
