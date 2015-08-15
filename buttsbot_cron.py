__author__ = 'Judson Dunaway-Barlow'

#Made with PRAW: https://praw.readthedocs.org/en/latest/
#Buttsbot original code at: https://github.com/jadunawa/ButtsBot

import os
import praw
import random
import sys
import sqlite3
import time
from datetime import datetime, date, timedelta

print str(datetime.now())

path_to_script=os.path.dirname(__file__)
#print path_to_script

#connect to sqlite database
conn=sqlite3.connect(path_to_script+'/links.db')
c=conn.cursor()

#c.execute('''CREATE TABLE permalinks
               # (link text)''')
conn.commit()

#get password
config_file=open(path_to_script+"/buttsbot_config.txt",'r')
un_line=config_file.readline()
un_string=un_line[4:-1]
pw_line=config_file.readline()
pw_string=pw_line[4:-1]

r = praw.Reddit(user_agent='I post butts!')
r.login(un_string, pw_string, disable_warning=True)

#TODO: Work on regex
#fuck regex
keywords = ['butt', 'booty', 'bootay', ' ass ',' ass.', 'ass?', 'ass,', 'keyster', 'heinie', 'hiney', 'derriere', 'posterior', 'arse', 'bottom', 'tush', 'rear.', ' rear ', 'rearend', 'bum', 'caboose', 'rump', 'fanny', 'glutes', 'badonkadonk']  # make list of words to trigger the comment reply
# TODO: Get a list of a bunch of imgur links to Astros Butts
butt_links=['Bagwell butt!](http://imgur.com/Vkx6fMI.jpg', 'Castro butt!](http://www.rantsports.com/mlb/files/2014/02/Jason-Castro-Houston-Astros.jpg',
            'Lowrie butt!](http://i.imgur.com/TwTi4DT.jpg', 'Conger butt!](http://i.imgur.com/P5C2BGK.jpg', 'Carlos Lee butt!](http://i.imgur.com/G5ZzVmp.jpg',
            'McHugh butt!](http://i.imgur.com/hClbvuL.jpg','Ausmus and Berkman butt!](http://i.imgur.com/mL5TtMx.jpg',
            'Minor Leagues Lowrie butt!](http://i.imgur.com/VTxAaqn.jpg','Kazmir butt!](http://imgur.com/ShvX5Xq.jpg',
            'Biggio butt!](http://i.imgur.com/7DlspmL.jpg','Biggio butt!](http://i.imgur.com/GYwHHxV.jpg','Marwin butt!](http://i.imgur.com/mqYVpy9.jpg',
            'Julia Morales butt!](http://imgur.com/SRzPWIJ.jpg','GoGo butt!](http://i.imgur.com/Xirtvvv.jpg',
            'Correa butt!](http://i.imgur.com/Y0JPeJK.jpg','Altuve butt!](http://i.imgur.com/bU64HWo.jpg',
            'Biggio bobble butt!](https://i.imgur.com/I3uavEH.jpg','Lance McButt!](http://i.imgur.com/tTUpRRm.jpg',
            'Marisnick butt! (from /u/Barrel-rider)](https://i.imgur.com/BerYpNo.jpg']

subreddit = r.get_subreddit('Astros')  # get /r/Astros

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
                talks_about_butts = any(string in l_comment for string in keywords)  #boolean for talking about butts
                # If the comment talks about butts and isn't a comment by this bot, respond with the correct string
                if talks_about_butts and str(comment.author)!="buttsbot":
                    print("Comment author: "+str(comment.author))
                    butt_number=random.randint(0,len(butt_links)-1)
                    full_reply="You have activated the Astros buttsbot! Here is a picture of [{}) Thanks for enjoying Astros buttocks! Go \'Stros!\n\nAny problems with this bot? Suggestions for more butts? Please send me a message!".format(butt_links[butt_number])
                    comment.reply(full_reply) #reply to the comment
                    comment.upvote() #upvote the comment
                    print("Replied to a comment: " +str(comment.permalink))
                c.execute('''INSERT INTO permalinks(link) VALUES (?)''',(perma,))
                conn.commit()
        print "-----------------------------------------------------------------"
    i += 1