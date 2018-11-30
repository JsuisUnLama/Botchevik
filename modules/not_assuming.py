from discord.ext import commands
from config.public import MAX_NOT_ASSUMING_SECONDS
from config.public import MIN_NOT_ASSUMING_SECONDS
from config.public import MAX_NOT_ASSUMING_NEXT_SECONDS
import asyncio


class NotAssuming:

    nan = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='na',
                      brief="Delete current message after x seconds",
                      description="Delete current message after x seconds",
                      usage="[seconds] The rest of your message")
    async def na(self, ctx, arg):
        if not arg.isdigit():
            return

        seconds = self._string_to_int(arg)

        await asyncio.sleep(seconds)
        await ctx.message.delete()

    @commands.command(name="nan",
                      brief="Delete the next message you write after x seconds",
                      description="Delete the next message after x seconds",
                      usage="seconds")
    async def nan(self, ctx, arg):
        pass



    @staticmethod
    def _string_to_int(string):
        seconds = int(string)

        if seconds == 0:
            seconds = MIN_NOT_ASSUMING_SECONDS

        if seconds > MAX_NOT_ASSUMING_SECONDS:
            seconds = MAX_NOT_ASSUMING_SECONDS

        return seconds


def setup(bot):
    bot.add_cog(NotAssuming(bot))
