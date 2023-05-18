import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import asyncio
import time
import logging

from apis import gmail
from settings import CHAT_IDS, CHAT_PW, BOT_TOKEN

logger = logging.getLogger(__name__)


# TODO make jobs persistent
class Trashbot():
    """Trashbot class"""

    def __init__(self):
        chat_ids = CHAT_IDS
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        service = gmail.authenticate()
    
        # add command handles
        handles = [('start', self.start), ('subscribe', self.subscribe) ] #('stop', stop)
        for handle in handles:
            application.add_handler(CommandHandler(handle[0], handle[1]))

        application.run_polling()


    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info('someone called start {}'.format(), extra={'update': update})
        greetingmsg = "Hallo liebe WG, ich bin da um euch an die Müllabfuhr zu erinnern : )"
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=greetingmsg
            )
    

    async def subscribe(self, update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
        pw = context.args[0]
        chat_id = update.message.chat_id

        if pw == CHAT_PW:
            await update.message.reply_text("Müllabfuhr incoming!")
            if self.service:
                # todo add chat id to subscriber list
                # add_subscriber(chat_id)
                pass
            else:
                await update.message.reply_text("Sorry, es gab einen Fehler bei der Gmail Authentifizierung")
    

    async def get_mails(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send the alarm message."""
        # chat_id, service = job.context
        mails = gmail.get_new_trashmails(self.service)
        for mail in mails:
            await context.bot.send_message(chat_id=CHAT_IDS, text=mail)


        

def run():
    """Run the bot."""
    # load previous chat ids that subscribed to trashbot
    
    # init telegram bot app
    trashbot = Trashbot()
    trashbot.

    # init gmail poll hook with send msg callback

    # add crash resistance