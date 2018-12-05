# Libraries
import logging


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


def standardized_error(error_msg, additional_info = ""):
    return '🚨 | **Error:** `{}`\n{}'.format(error_msg, ("" if additional_info == "" else "🔸 | {}".format(additional_info)))