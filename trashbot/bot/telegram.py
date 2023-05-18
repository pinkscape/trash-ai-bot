import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import logging

from apis import gmail
from settings import CHAT_IDS, CHAT_PW, BOT_TOKEN

logger = logging.getLogger(__name__)



async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Müllabfuhr abbestellt : )"
        ) 





def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True



def stop(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    pw = context.args[0]
    if pw == CHAT_PW:
        job_removed = remove_job_if_exists("trashbot", context)
        text = 'Müllabfuhr abbestellt : )' if job_removed else 'Du hast den Mailreminder nicht aktiviert'
        update.message.reply_text(text)


async def main():
    bot = telegram.Bot()
    async with bot:
        update_msgs = (await bot.get_updates())[0]
        logger.info(update_msgs)


def run():
    # init application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # add command handles
    handles = [('start', start), ('sendmails', sendmails), ('stop', stop)]
    for handle in handles:
        application.add_handler(CommandHandler(handle[0], handle[1]))

    application.run_polling()
