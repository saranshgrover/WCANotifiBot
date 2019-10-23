import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(bot, update):
    update.effective_message.reply_text("Hello, I am the Comp Scheduler Bot. To be notified for a competition, run /schedule <CompID>")


def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)

def schedule(update,context):
    #comp_id = " ".join(context.args)
    update.effective_message.reply_text("yousaidschedule")#"Fetching schedule for " + comp_id)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = os.environ.get('TOKEN','993159315:AAFA_cNylEFenK_X1_SwMKk0RjoCNGUkFpk')
    NAME = "hidden-lake-02945"

    # Port is given by Heroku
    PORT = os.environ.get('PORT',8857)

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('schedule', schedule))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
