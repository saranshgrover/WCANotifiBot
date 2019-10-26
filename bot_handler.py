import requests
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, InlineQueryHandler, JobQueue
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
import telegram
import datetime
import constants
from comp_notif import comp_notif
import dateutil.parser, dateutil.tz

class bot_handler:
    """Class that handles the commands called by a user to the bot. Creates, maintains and updates
    the comp_notif instance as needed.
    """


    def __init__(self,logger,updater: Updater,jobs: JobQueue, testing: bool):
        """Initializer. Stores the logger globally and also creates an empty dictionary to store
        compeition ids and their respective comp_notif class instances.
        
        Arguments:
            logger {[telgram.Logger]} -- [logger created in main]
        """
        self.logger = logger
        self.jobs = jobs
        self.comps = dict()
        self.testing = testing

    def stop(self, update: Update, context: CallbackContext):
        """Called to stop notifications for a competition.
        
        Arguments:
            update {Update}
            contet {CallbackContext}
        """
        if context.args == []:
            self.reply(update,constants.stop_invalid_id)
            return
        query = context.args[0]
        if query in self.comps:
            self.comps.pop(query)
            self.reply(update,constants.stop_removed_id.format(query))
        else:
            self.reply(update,constants.stop_invalid_id)
        
    def help(self,update: Update, context: CallbackContext):
        """Returns a list of commands and instructions
        
        Arguments:
            update {Update}
            context {CallbackContext}
        """
        self.reply(update,constants.help_me)
    def reply(self, update: Update, text: str):
        """Sends a reply message to Update
        
        Arguments:
            update {Update}
            text {str} -- [String to reply]
        """
        return update.message.reply_text(text,parse_mode=telegram.ParseMode.MARKDOWN)


    def start(self,update: Update, context: CallbackContext):
        """Called when "/start" command is called. Validates the competition ID. Makes a get
        request, creates the comp_notif instance and adds the comp to the dictionary. If 
        invalid comp ID, updates the user. 
        
        Arguments:
            update {Update}
            context {CallbackContext}
        """
        bot = context.bot
        if context.args == []:
            self.reply(update,constants.start_invalid_id)
            return
        query = context.args[0]
        if query in self.comps:
            self.reply(update,constants.start_already_begun.format(query))
            return
        url = constants.wca_api_schedule_url.format(context.args[0])
        res = requests.get(url)
        schedule = res.json()
        if 'error' in schedule:
            self.reply(update,constants.start_invalid_id)
            return
        end_date = datetime.datetime.strptime(schedule["startDate"],"%Y-%m-%d") + datetime.timedelta(days=int(schedule["numberOfDays"])-1)
        if(datetime.timedelta(days=7)>end_date-datetime.datetime.today()<datetime.timedelta(days=-1)):
            self.reply(update,constants.start_invalid_date) 
            return
        compNotif = comp_notif(query,schedule)
        try:
            message = context.bot.send_message(chat_id="@{}".format(query),text="Welcome to {}. Settle down, you will be alerted when a new group starts. Courtesey of @wcanotifbot".format(query))
            context.bot.pinChatMessage(chat_id="@{}".format(query),message_id=message.message_id)
        except Exception as e:
            print(e)
            self.reply(update,constants.start_not_admin.format(query))
            return
        self.comps[query] = compNotif
        self.add_jobs(compNotif.notifications,compNotif)
        self.reply(update,constants.start_notifcations.format(query))

    def add_jobs(self,jobs_to_add: list, comp_notif: comp_notif):
        """Adds a list of jobs to the job queue
        
        Arguments:
            jobs_to_add {list} -- list of jobs
        """
        n = 10
        for jobs in jobs_to_add:
            time = dateutil.parser.parse(jobs['startTime'])
            time = time.replace(tzinfo=None)
            job = self.jobs.run_once(comp_notif.job_callback,n if self.testing else time,context=jobs)
            comp_notif.add_job(job)
            n+=10
    def notification(self,update,context):
        query = update.inline_query.query
        url = "https://www.worldcubeassociation.org/api/v0/competitions/" + query + "/schedule"
        res = requests.get(url)
        schedule = res.json()
        if 'error' in schedule:
            return
        results = list()
        results.append(
            InlineQueryResultArticle(
                id=query.upper(),
                title='Start Notifications',
                input_message_content=InputTextMessageContent(query.upper())
            )
        )
        context.bot.answer_inline_query(update.inline_query.id, results)
    def error(self,bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)