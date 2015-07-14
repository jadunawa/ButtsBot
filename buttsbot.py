__author__ = 'judsondb'

import praw
import time
from datetime import datetime, date, timedelta
from pprint import pprint

r=praw.Reddit(user_agent='Test script by /u/jdb12')
r.login('buttsbot','gostros',disable_warning=True)
top10=r.get_subreddit('astros').get_hot(limit=10)
'''for i in range(0,10):
    #print(i)
    subm_title=next(top10).title
    if(subm_title[:12]=="Game Thread:"):
        print()
        #print(subm_title)'''

#TODO: Figure out how to see if dates are within 24 hours of each other
print time.strftime("%m/%d/%Y")
print datetime.now()
print datetime.now()-timedelta(1)

#Make list of comment permalinks
already_checked=[]

keywords=['butt','butts','booty','buttcheeks','keyster','heinie']
reply_string='#THIS BOT IS STILL IN DEVELOPMENT\n\nYou have activated the Astros\' buttsbot! Here is a picture of an [Astros butt!](http://www.rantsports.com/mlb/files/2014/02/Jason-Castro-Houston-Astros.jpg) Thanks for enjoying Astros buttocks! Go \'Stros!\n\nAny problems with this bot? Please send a message to /u/jdb12.'

while True:
    i=1
    subreddit=r.get_subreddit('Astros')
    for submission in subreddit.get_hot(limit=20):
        #TODO: if post is over 24 hours old, ignore it as well
        print('Testing submission ',i)
        submission.replace_more_comments(limit=None, threshold=0)
        all_comments=submission.comments
        flaternized_comments=praw.helpers.flatten_tree(all_comments)
        print(submission.created_utc)
        print datetime.fromtimestamp(int(submission.created_utc))
        for comment in flaternized_comments:
            if(comment.permalink not in already_checked):
                l_comment=str(comment).lower()
                talks_about_butts=any(string in l_comment for string in keywords)
                #TODO: Make sure it doesn't respond to itself
                if talks_about_butts:
                    #comment.reply(reply_string)
                    print("true")
                already_checked.append(comment.permalink)
        i+=1
        print "-----------------------------------------------------------------"
    time.sleep(5)
    #break