import logging

log = logging.getLogger(__name__)

class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)

        log_msg = f"The message : '{ctx.message.content}' posted by {str(ctx.author)} generated the following error : {str(error)}"
        log.error(log_msg)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))