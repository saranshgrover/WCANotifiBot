import requests
import datetime
import operator
from telegram.ext import CallbackContext
import telegram
import constants
import random
class comp_notif:
    """Class to wrap the notification list for a competition
    """
    def __init__(self,comp_id,comp_schedule):
        # set id
        self.competition_id = comp_id
        self.schedule = comp_schedule
        self.get_activities(comp_schedule)
        self.jobs = []

    def add_job(self,job):
        self.jobs.append(job)

    def job_callback(self,context: CallbackContext):
        job = context.job
        notif = job.context
        announcement = constants.which_announcement(notif['activityCode'])
        text = random.choice(announcement).format(notif['name'])
        context.bot.send_message(chat_id="@{}".format(self.competition_id),text=text,parse_mode = telegram.ParseMode.MARKDOWN)
        self.jobs.remove(job)


    def get_activities(self,schedule):
        """takes a json schedule and returns a list of activities to be notified on in ascending order
        
        Arguments:
            schedule {[json]} -- schedule of competition
        """
        self.notifications = []
        for venue in schedule["venues"]:
            for room in venue["rooms"]:
                for activity in room["activities"]:
                    self.notifications.append(activity)
                    for childActivity in activity["childActivities"]:
                        self.notifications.append(childActivity)
        self.notifications.sort(key=operator.itemgetter('startTime'))
        for notification in self.notifications:
            print(notification['name'])
    
        
        
       
       