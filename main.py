import logging
import os
import requests
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from bot_handler import bot_handler
import constants

if __name__ == "__main__":
    testing = False
    # Set these variable to the appropriate values
    TOKEN = os.environ.get('TOKEN',constants.name_test_token)
    if(TOKEN==constants.name_test_token):  
        testing = True
    NAME = constants.name_heroku
    # Port is given by Heroku
    PORT = os.environ.get('PORT',5500)

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    # Set up the Updater
    updater = Updater(TOKEN,use_context=True)
    # dispatcher
    dp = updater.dispatcher
    # job queue
    jobs = updater.job_queue
    # Create Instance of Bot Handler
    handle = bot_handler(logger,updater,jobs,testing)
    # Add handlers
    start_handler = CommandHandler('start',handle.start)
    stop_hanlder = CommandHandler('stop',handle.stop)
    help_handler = CommandHandler('help',handle.help)
    dp.add_handler(start_handler)
    dp.add_handler(stop_hanlder)
    dp.add_handler(help_handler)
    dp.add_error_handler(handle.error)

    # Start the webhook
    
    if testing:
        updater.start_polling()
    else:
        updater.start_polling()
        """updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN)
        updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
        updater.idle()"""
