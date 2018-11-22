from discord.ext import commands
from config.secrets import TOKEN
import logging

description = 'Bot tailored for Git Gud.'
bot = commands.Bot(command_prefix='-', description=description)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

module_bot = [
    #'flood',
    'lewd',
    #'meme',
    #'na',
    'pikachuface',
    #'remind'
]

if __name__ == '__main__':
    for ext in module_bot:
        try:
            bot.load_extension('modules.' + ext)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(ext, exc))

bot.run(TOKEN)