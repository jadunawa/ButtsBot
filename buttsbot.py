__author__ = 'Judson Dunaway-Barlow'

import praw
import sys
import sqlite3
import time
from datetime import datetime, date, timedelta

#connect to sqlite database
conn=sqlite3.connect('links.db')
c=conn.cursor()

#c.execute('''CREATE TABLE permalinks
               # (link text)''')
conn.commit()

#get password
config_file=open("buttsbot_config.txt",'r')
un_line=config_file.readline()
un_string=un_line[4:-1]
pw_line=config_file.readline()
pw_string=pw_line[4:-1]

r = praw.Reddit(user_agent='ButtsBot!')
r.login(un_string, pw_string, disable_warning=True)
top10 = r.get_subreddit('astros').get_hot(limit=10)

already_checked = []  # make list of comment permalinks

keywords = ['butt', 'booty', 'buttcheeks', 'keyster', 'heinie']  # make list of words to trigger the comment reply
# TODO: Get a list of a bunch of imgur links to Astros Butts

reply_string = 'You have activated the Astros\' buttsbot! Here is a picture of an [Astros butt!](http://www.rantsports.com/mlb/files/2014/02/Jason-Castro-Houston-Astros.jpg) Thanks for enjoying Astros buttocks! Go \'Stros!\n\nAny problems with this bot? Please send me a message!'

subreddit = r.get_subreddit('Astros')  # get /r/Astros

while True:
    i = 1
    # go through top 20 submissions of /r/Astros
    for submission in subreddit.get_hot(limit=20):
        submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date
        day_ago = datetime.fromtimestamp(time.time() - (24 * 60 * 60))  # find date for 24 hours ago
        # ignore posts over 24 hours old
        if (int((day_ago - submission_date).days) + 1< 2):
            print('Testing submission ', i)
            print(day_ago - submission_date).days
            submission.replace_more_comments(limit=None, threshold=0)  # get all comments instead of just first few
            all_comments = submission.comments  # make array of comments
            flaternized_comments = praw.helpers.flatten_tree(all_comments)  # ignore tree structure of comments
            # Iterate through comments in the submission
            for comment in flaternized_comments:
                # Ignore comments that have already been checked to avoid multiple replies to the same comment
                perma=str(comment.permalink)
                if (str(c.execute("SELECT link FROM permalinks WHERE link='{}'".format(perma)).fetchone())=="None"):
                    print "NONE OMG THIS WORKS"
                    l_comment = str(comment).lower()  # make the comment lowercase
                    talks_about_butts = any(string in l_comment for string in keywords)  # set up boolean for talking about butts
                    # If the comment talks about butts and isn't a comment by this bot, respond with the correct string
                    if talks_about_butts and str(comment.author)!="buttsbot":
                        print("Comment author: "+str(comment.author))
                        # TODO: Randomize which imgur link is posted as part of the reply string using a new function
                        comment.reply(reply_string) #reply to the comment
                        print("Replied to a comment: " +str(comment.permalink))
                    already_checked.append(comment.permalink)  # add comment to already_checked
                    c.execute('''INSERT INTO permalinks(link) VALUES (?)''',(perma,))
                    conn.commit()
            print "-----------------------------------------------------------------"
        i += 1
    print("Sleeping for a minute")
    time.sleep(60)  # sleep for a little bit to allow time for new comments to be made