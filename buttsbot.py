__author__ = 'Judson Dunaway-Barlow'

import praw
import sys
import time
from datetime import datetime, date, timedelta

r = praw.Reddit(user_agent='Test script by /u/jdb12')
r.login('buttsbot', 'gostros', disable_warning=True)
top10 = r.get_subreddit('astros').get_hot(limit=10)

already_checked = []  # make list of comment permalinks

keywords = ['butt', 'butts', 'booty', 'buttcheeks', 'keyster',
            'heinie']  # make list of words to trigger the comment reply
# TODO: Get a list of a bunch of imgur links to Astros Butts

reply_string = '#THIS BOT IS STILL IN DEVELOPMENT\n\nYou have activated the Astros\' buttsbot! Here is a picture of an [Astros butt!](http://www.rantsports.com/mlb/files/2014/02/Jason-Castro-Houston-Astros.jpg) Thanks for enjoying Astros buttocks! Go \'Stros!\n\nAny problems with this bot? Please send a message to /u/jdb12.'

subreddit = r.get_subreddit('Astros')  # get /r/Astros

while True:
    i = 1
    # go through top 20 submissions of /r/Astros
    for submission in subreddit.get_hot(limit=20):
        print('Testing submission ', i)
        submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date
        day_ago = datetime.fromtimestamp(time.time() - (24 * 60 * 60))  # find date for 24 hours ago
        # ignore posts over 24 hours old
        if (int((date_one - date_two).days) < 2):
            print("Got here")
            sys.exit(0)
            submission.replace_more_comments(limit=None, threshold=0)  # get all comments instead of just first few
            all_comments = submission.comments  # make array of comments
            flaternized_comments = praw.helpers.flatten_tree(all_comments)  # ignore tree structure of comments
            # Iterate through comments in the submission
            for comment in flaternized_comments:
                # TODO: Ignore comments over 24 hours old
                # Ignore comments that have already been checked to avoid multiple replies to the same comment
                if (comment.permalink not in already_checked):
                    l_comment = str(comment).lower()  # make the comment lowercase
                    talks_about_butts = any(
                        string in l_comment for string in keywords)  # set up boolean for talking about buts
                    # print comment.created_utc
                    # TODO: Make sure it doesn't respond to itself
                    # If it talks about butts, respond with the correct string
                    if talks_about_butts:
                        # TODO: Randomize which imgur link is posted as part of the reply string using a new function
                        # comment.reply(reply_string) #reply to the comment
                        print("Replied to a comment")
                    already_checked.append(comment.permalink)  # add comment to already_checked
        i += 1
        print "-----------------------------------------------------------------"
    time.sleep(5)  # sleep for a little bit to allow time for new comments to be made