import sqlite3
import uuid
from datetime import datetime

from discord import Embed, Colour
from discord.ext import commands
from utils.errormanager import standardized_error
from config.public import DATABASE_NAME
import discord
import asyncio
import logging
import dateparser


log = logging.getLogger(__name__)


class Remind:

    def __init__(self, bot):
        self.rmdb = ReminderDB()
        self.bot  = bot
        self.reminders = self.rmdb.get_reminders()

    @commands.command(name='premind',
                      aliases=["premindme"],
                      brief='Personal remind at a certain date',
                      description="Ask the bot to send you the private message <str> tomorrow [or at date <date>] same hour.",
                      usage="[date] <str>")
    async def premind(self, ctx,  date: str, *, text_to_remind: str):
        """Sends you <str> when the time is up

        Accepts: Everything that dateparser can parse (https://dateparser.readthedocs.io/en/latest/)
        Example:
        premind "in 3 days" Hello me from the future !"""

        author      = ctx.message.author
        remind_date = dateparser.parse(date, settings={'STRICT_PARSING': True})

        if remind_date is None:
            await ctx.send(standardized_error("Wrong date ! Please see : https://dateparser.readthedocs.io/en/latest/", "The date you inputted : `{}`".format(date)))
            return

        if datetime.now() >= remind_date:
            await ctx.send(standardized_error("You can't register a remind in the past, you need to use D-mail for that !"))
            return

        embed = Embed(color=Colour.dark_green(), title="📅 **Personal reminder**", description="Reminder successfully registered")
        embed.add_field(name="Date", value='`{}`'.format(remind_date.strftime("%d %B %Y %H:%M:%S")))
        embed.add_field(name="Text", value='`{}`'.format(text_to_remind), inline=False)
        await ctx.send(embed=embed)

        self.register_reminder(author, remind_date, text_to_remind)
        log.info("{} ({}) set a reminder.".format(author.name, author.id))

    async def check_reminders(self):
        """
        Function that is called every 60 seconds to check if a reminder must be send
        """
        while self is self.bot.get_cog("Remind"):
            to_remove = []
            for reminder in self.reminders:
                if reminder["date"] <= datetime.now():
                    try:
                        user = self.bot.get_user(reminder["author_id"]) or (await self.bot.get_user_info(reminder["author_id"]))
                        embed = Embed(color=Colour.red(), title="⏰ **Personal reminder**", description="You asked me to remind you this")
                        embed.add_field(name="Message", value='`{}`'.format(reminder["text"]))
                        await user.send(embed=embed)
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(reminder)
                    except discord.errors.HTTPException:
                        pass
                    else:
                        to_remove.append(reminder)

            for reminder in to_remove:
                self.remove_reminders(reminder)

            await asyncio.sleep(60)

    def register_reminder(self, author, remind_date, text_to_remind):
        uuid_str = str(uuid.uuid4())  # Generate UUID because of the database
        reminder = {"author_id": author.id, "date": remind_date, "text": text_to_remind, 'uuid': uuid_str}
        self.reminders.append(reminder)
        self.rmdb.add_reminder(reminder)

    def remove_reminders(self, remind):
        self.reminders.remove(remind)
        self.rmdb.remove_reminder(remind)


class ReminderDB:
    def __init__(self):
        self.db  = sqlite3.connect(DATABASE_NAME)
        self.cur = self.db.cursor()

    def get_reminders(self):
        try:
            val = []
            self.cur.execute("SELECT uuid_reminder, date_reminder as 'ts [timestamp]', author_reminder, text_reminder FROM reminders;")
            res = self.cur.fetchall()
            for row in res:
                val.append({"uuid": row[0], "date": dateparser.parse(row[1]), "author_id": row[2], "text": row[3]})
            return val
        except Exception as e:
            log.error("Error in 'get_reminders_from_db' : " + str(e))
            return []

    def add_reminder(self, reminder):
        try:
            sql = "INSERT INTO reminders(uuid_reminder, date_reminder, author_reminder, text_reminder) VALUES(:uuid, :date, :author_id, :text)"
            self.cur.execute(sql, reminder)
            self.db.commit()
        except Exception as e:
            log.error("Error in 'add_reminder_to_db' : " + str(e))

    def remove_reminder(self, remind):
        try:
            sql = "DELETE FROM reminders WHERE uuid_reminder = ?"
            self.cur.execute(sql, (remind['uuid'],))
            self.db.commit()
        except Exception as e:
            log.error("Error in 'remove_reminder_from_db' : " + str(e))


def setup(bot):
    n = Remind(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.check_reminders())
    bot.add_cog(n)
