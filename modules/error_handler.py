import logging
from discord.ext import commands
log = logging.getLogger(__name__)

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)

        log_msg = f"The message : '{ctx.message.content}' posted by {str(ctx.author)} generated the following error : {str(error)}"
        log.error(log_msg)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))