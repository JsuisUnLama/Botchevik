# Libraries
from random import randint
from random import uniform
from discord.ext import commands
import logging
import asyncio
from config.public import FLOOD_COOLDOWN_TIME
from config.public import NUMBER_OF_SUPER_MESSAGE
from config.public import MIN_NUMBER_OF_MESSAGE
from config.public import MAX_NUMBER_OF_MESSAGE
from config.public import MIN_NUMBER_OF_PARTS
from config.public import MAX_NUMBER_OF_PARTS
from config.public import MIN_QUESTION_MARKS_PER_PARTS
from config.public import MAX_QUESTION_MARKS_PER_PARTS
from config.public import RANDOM_WTF_CHANCE
from config.public import RANDOM_SPACE_CHANCE
from config.public import WAITING_TIME_BEFORE_DELETION

# Create logger
log = logging.getLogger(__name__)

# Class
class QuestionMarkFlood:

    # Init
    def __init__(self, bot):
        self.bot = bot

    # Command meme declaration
    @commands.cooldown(rate=1,per=FLOOD_COOLDOWN_TIME)
    @commands.command(name='xQc chat', 
                      aliases=['xQc?','xqc?','???','wtf','wtf?'],
                      brief='??????????????????????????',
                      description="floods chat with question marks",
                      usage="['clip']")
    async def meme(self, ctx, clip = "no"):

        # No clip
        if clip != "clip": 
            members_list = ctx.guild.members
            nb_members = len(members_list)-1
            messages = []

            for i in range (0,NUMBER_OF_SUPER_MESSAGE):
                super_message = ""
                
                nb_of_messages = randint(MIN_NUMBER_OF_MESSAGE, MAX_NUMBER_OF_MESSAGE)
                for j in range (0,nb_of_messages):
                    member = members_list[randint(0,nb_members)].name
                    message = member + ': '

                    if round(uniform(0.0,1.0),1) <= RANDOM_WTF_CHANCE:
                        message += 'WTF   '

                    nb_of_parts = randint(MIN_NUMBER_OF_PARTS,MAX_NUMBER_OF_PARTS)
                    for k in range (0,nb_of_parts):

                        number_of_qm = randint(MIN_QUESTION_MARKS_PER_PARTS,MAX_QUESTION_MARKS_PER_PARTS)
                        for l in range (0,number_of_qm):
                            message+='?'

                            if round(uniform(0.0,1.0),2) <= RANDOM_SPACE_CHANCE:
                                message += '   '

                        message+=' '
                    
                    super_message += message + "\n"

                messages.append(super_message)

            messages_sent = []
            for m in messages:
                message_sent = await ctx.send(m)
                messages_sent.append(message_sent)
                async_sleep = round(uniform(0.5,1.5),1)
                await asyncio.sleep(async_sleep)

            await asyncio.sleep(WAITING_TIME_BEFORE_DELETION)
            await ctx.channel.delete_messages(messages_sent)

        # Clip
        else:
            await ctx.send("Soon (v2 feature)")

# Setup
def setup(bot):
    bot.add_cog(QuestionMarkFlood(bot))