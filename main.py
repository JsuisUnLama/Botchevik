from discord.ext import commands
from config.secrets import TOKEN
from time import gmtime
import logging

description = 'Bot tailored for Git Gud.'
bot = commands.Bot(command_prefix='-', description=description)


logging.getLogger('discord').setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.WARNING)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='botchevik.log', encoding='utf-8', mode='a')
formatter = logging.Formatter('[%(asctime)s UTC] [%(levelname)s] %(name)s: %(message)s', '%Y-%m-%d %H:%M:%S')
formatter.converter = gmtime
handler.setFormatter(formatter)
logger.addHandler(handler)

module_bot = [
    'event',
    'flood',
    'lewd',
    'audiomeme',
    'not_assuming',
    'pikachuface',
    'remind',
    'error_handler',
    'misc'
]

if __name__ == '__main__':
    for ext in module_bot:
        try:
            bot.load_extension('modules.' + ext)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(ext, exc))

bot.run(TOKEN)