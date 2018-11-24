from discord.ext import commands
from config.public import MAX_NOT_ASSUMING_SECONDS
import asyncio


class NotAssuming:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='na',
                      brief="Delete current message after x seconds",
                      description="Delete current message after x seconds",
                      usage="seconds [The rest of your message]")
    async def na(self, ctx, arg):
        if not arg.isdigit():
            return

        seconds = int(arg)

        if seconds == 0:
            seconds = 1

        if seconds > MAX_NOT_ASSUMING_SECONDS:
            seconds = MAX_NOT_ASSUMING_SECONDS

        await asyncio.sleep(seconds)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(NotAssuming(bot))
