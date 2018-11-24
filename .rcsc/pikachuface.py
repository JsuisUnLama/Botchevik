# Command: pf
# Arguments: [type | int]
# Description: post a pikachu face [of insanity level [int] or of type [type]]
# Author: @JsuisUnLama

# Libraries
from discord.ext import commands
import sqlite3

class PikachuFace:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pf', pass_context=True)
    async def pf(self, ctx, attr = "0"):
        try:
            conn = sqlite3.connect('data/users.db')
            cursor = conn.cursor()
            name = "pf_" + (attr.isdigit() ? "il" : "") + attr
            cursor.execute("""SELECT image_pika FROM pikachus WHERE name_pika = name""")
            if(cursor.fetchone()[0] == ""):
                print('Error: couldn\'t fetch any pikachu; ' + attr + 'haven\'t been recognized')
            else:
                conn.commit()
        except sqlite3.OperationalError:
            print('Error: table doesn\'t exist')
        except Exception as e:
            print("Error")
            conn.rollback()
            # raise e
        finally:
            conn.close()
        
def setup(bot):
bot.add_cog(PikachuFace(bot))