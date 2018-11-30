# Libraries
import logging
import discord
from discord import Embed
from discord import Colour

# Create logger
log = logging.getLogger(__name__)

# Log manager
def manageLog(self, ctx, logUsage = 'l', logMsg = "Something went wrong"):
    if logUsage is 'l':
        log.log(logMsg)
    elif logUsage is 'w':
        log.warning(logMsg)
    else:
        log.error(logMsg)
    return

# Error manager
async def manageErr(self, ctx, errMsg = "Error", additionalInfo = ""):
    await ctx.send('⚠    **Error:**    ⚠\n ' + errMsg + '\n' + additionalInfo)
    return