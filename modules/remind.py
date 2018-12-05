import sqlite3
import uuid
from datetime import datetime, timezone, timedelta

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
        self.p_reminders = self.rmdb.get_reminders()



    @commands.command(name='premind',
                      aliases=["premindme"],
                      brief='Personal remind at a certain date',
                      description="Ask the bot to send you the private message <str> tomorrow [or at date <date>] same hour.",
                      usage="[date] <str>")
    async def p_remind(self, ctx,  date: str, *, text_to_remind: str):
        """Sends you <str> when the time is up

        Accepts: Everything that dateparser can parse (https://dateparser.readthedocs.io/en/latest/)
        Example:
        premind "in 3 days" Hello me from the future !"""

        author        = ctx.message.author
        is_valid, res = self._is_valid_date(date)

        if not is_valid:
            await ctx.send(standardized_error(res))
            return

        embed = Embed(color=Colour.dark_green(), title="📅 **Personal reminder**", description="Reminder successfully registered")
        embed.add_field(name="Date", value='`{} UTC`'.format(res.strftime("%d %B %Y %H:%M:%S")))
        embed.add_field(name="Text", value='`{}`'.format(text_to_remind), inline=False)
        await ctx.send(embed=embed)

        self.register_reminder(author.id, res, text_to_remind, author.id)
        log.info("{} ({}) set a reminder.".format(author.name, author.id))


    @commands.command(name='remind',
                      aliases=["remindus", "repeat"],
                      brief='Repeat a message every [x] hours until [date]',
                      description="Repeat a message with a specified interval until a specified date on the channel the command is executed",
                      usage="[float:interval (in hour)][date: (valid dateparser date)] <str: message>")
    async def reminder(self, ctx, interval: float, date: str, *, text_to_remind: str):
        channel_id    = ctx.channel.id
        is_valid, res = self._is_valid_date(date)
        print(ctx.message.mentions)
        print(ctx.message.role_mentions)
        print(text_to_remind)

        if not is_valid:
            await ctx.send(standardized_error(res))
            return

        if interval <= 0:
            await ctx.send(standardized_error("Please specify an interval that is greater than zero"))
            return

        embed = Embed(color=Colour.dark_blue(), title="🔄 **Reminder**", description="Reminder successfully registered")
        embed.add_field(name="Interval", value='`{} hours`'.format(interval))
        embed.add_field(name="Finish Date", value='`{} UTC`'.format(res.strftime("%d %B %Y %H:%M:%S")), inline=False)
        embed.add_field(name="Text", value='`{}`'.format(text_to_remind), inline=False)
        await ctx.send(embed=embed)

        self.register_reminder(channel_id, res, text_to_remind, ctx.message.author.id, interval=interval)
        log.info("{} ({}) set a periodic reminder.".format(ctx.message.author.name, ctx.message.author.id))



    async def check_reminders(self):
        """
        Function that is called every 60 seconds to check if a reminder must be or deleted
        """
        while self is self.bot.get_cog("Remind"):
            to_remove = []
            for reminder in self.p_reminders:
                if reminder["date"] <= datetime.utcnow():
                    if reminder["interval"] == 0: #Personal Remind only
                        try:
                            user = self.bot.get_user(reminder["channel"]) or (await self.bot.get_user_info(reminder["channel"]))
                            embed = Embed(color=Colour.red(), title="⏰ **Personal reminder**", description="You asked me to remind you this")
                            embed.add_field(name="Message", value='`{}`'.format(reminder["text"]))
                            await user.send(embed=embed)
                        except Exception as e:
                            log.error("Error in check_reminders : " + str(e))

                    to_remove.append(reminder)
                    continue

                if reminder["interval"] > 0: # Periodic Remind only
                    now    = datetime.utcnow()
                    start  = reminder["created_at"]
                    tdelta = (now - start).seconds
                    if tdelta <= 60:
                        continue

                    hours  = tdelta/3600
                    modulo = hours % float(reminder["interval"])

                    if modulo >= 0.0 and modulo <= (1 / 60): # Error margin because it's executed every minute
                        print(modulo)
                        ch = self.bot.get_channel(int(reminder["channel"]))
                        print(ch)
                        embed = Embed(color=Colour.dark_red(), title="⏲ **Periodic reminder**", description="<@{}> asked me to remind you the message above".format(reminder["author"]))
                        await ch.send(content=reminder["text"],embed=embed)

            for reminder in to_remove:
                self.remove_reminder(reminder)

            await asyncio.sleep(60)


    def register_reminder(self, channel, remind_date, text_to_remind, author_id, interval=0.0):
        uuid_str = str(uuid.uuid4())  # Generate UUID because of the database
        cdate    = datetime.utcnow()
        reminder = {
            'channel': str(channel),
            'date': remind_date,
            'text': text_to_remind,
            'uuid': uuid_str,
            'interval': interval,
            'created_at': cdate,
            'author': author_id
        }
        self.p_reminders.append(reminder)
        self.rmdb.add_reminder(reminder)


    def remove_reminder(self, remind):
        self.p_reminders.remove(remind)
        self.rmdb.remove_reminder(remind)


    def _is_valid_date(self, date_to_parse):
        parsed_date = dateparser.parse(date_to_parse, settings={'STRICT_PARSING': True, 'TO_TIMEZONE': 'UTC'})

        if parsed_date is None:
            str = "Wrong date ! Please see : https://dateparser.readthedocs.io/en/latest/", "The date you inputted : `{}`".format(date_to_parse)
            return (False, str)

        if datetime.utcnow() >= parsed_date:
            str = "You can't register a remind in the past, you need to use D-mail for that !"
            return (False, str)

        if parsed_date > (datetime.utcnow() + timedelta(days=40)):
            str = "You can only register a remind in the following 40 days"
            return (False, str)

        return (True, parsed_date)


class ReminderDB:

    def __init__(self):
        self.db  = sqlite3.connect(DATABASE_NAME)
        self.cur = self.db.cursor()

    def get_reminders(self):
        try:
            val = []
            self.cur.execute("SELECT uuid_reminder, date_reminder as 'ts [timestamp]', channel_reminder, text_reminder, interval_reminder, creation_reminder, author_reminder FROM reminders;")
            res = self.cur.fetchall()
            for row in res:
                val.append({
                    "uuid": row[0],
                    "date": dateparser.parse(row[1]),
                    "channel": row[2],
                    "text": row[3],
                    "interval": row[4],
                    "created_at": dateparser.parse(row[5]),
                    "author": int(row[6])
                })
            return val
        except Exception as e:
            log.error("Error in 'get_reminders_from_db' : " + str(e))
            return []


    def add_reminder(self, reminder):
        try:
            sql = "INSERT INTO reminders(uuid_reminder, date_reminder, channel_reminder, text_reminder, interval_reminder, creation_reminder, author_reminder) " \
                  "VALUES(:uuid, :date, :channel, :text, :interval, :created_at, :author)"
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
