import re

# URLS
wca_api_schedule_url ="https://www.worldcubeassociation.org/api/v0/competitions/{}/schedule"

# Start Responses
start_invalid_id = "/start requires a valid WCA Competition ID. Please enter one"
start_already_begun = "Already started notifications for {}. Please use /stop to start again"
start_notifcations = "Starting notifications for: {}"
start_invalid_date = "This competition is over. Please enter a future or current competition only"

# Names

name_heroku = "hidden-lake-02945"
name_test_token = '1004653031:AAGip5QUdASk1hBmiy2R4u-TjMCyGNu31To'
name_app = "WCA Competition Notifier"

# Annoucmenets

event_start = [
    "We are now moving on to the next event: *{}*",
    "Are you in *{}*? Well, its about to start. Grab your hand warmers",
    "Get your last couple solves in, {} is about to begin"
]

lunch_start = [
    "I hear some growls. No worries, *{}* just began!",
    "Alright friends, off to *{}*.",
    "What did the droid do at *{}* time? \n Had a byte!"
]

group_start = [
    "Now calling *{}*",
    "Are you in *{}*? Bring your puzzle to the drop off table."
]

generic_announcement = [
    "Now beginning *{}*"
]

def which_announcement(activity):
    if re.search("^other-lunch$",activity):
        return lunch_start
    elif re.search("^other.*$",activity):
        return generic_announcement
    elif re.search("^.*-r\d$",activity):
        return event_start
    elif re.search("^.*-r\d-g\d$",activity):
        return group_start
