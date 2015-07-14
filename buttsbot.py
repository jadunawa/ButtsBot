__author__ = 'Judson Dunaway-Barlow'

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
#TODO: Get a list of a bunch of imgur links to Astros Butts

reply_string='#THIS BOT IS STILL IN DEVELOPMENT\n\nYou have activated the Astros\' buttsbot! Here is a picture of an [Astros butt!](http://www.rantsports.com/mlb/files/2014/02/Jason-Castro-Houston-Astros.jpg) Thanks for enjoying Astros buttocks! Go \'Stros!\n\nAny problems with this bot? Please send a message to /u/jdb12.'

while True:
    i=1
    subreddit=r.get_subreddit('Astros')
    #TODO: Ignore posts over 24 hours old
    #Go through top 20 submissions
    for submission in subreddit.get_hot(limit=20):
        print('Testing submission ',i)
        submission.replace_more_comments(limit=None, threshold=0) #get all comments instead of just first few
        all_comments=submission.comments #make array of comments
        flaternized_comments=praw.helpers.flatten_tree(all_comments) #ignore tree structure of comments
        print(submission.created_utc)
        print datetime.fromtimestamp(int(submission.created_utc))
        #Iterate through comments in the submission
        for comment in flaternized_comments:
            #TODO: Ignore comments over 24 hours old
            #Ignore comments that have already been checked to avoid multiple replies to the same comment
            if(comment.permalink not in already_checked):
                l_comment=str(comment).lower() #make the comment lowercase
                talks_about_butts=any(string in l_comment for string in keywords) #set up boolean for talking about buts
                print comment.created_utc
                #TODO: Make sure it doesn't respond to itself
                #If it talks about butts, respond with the correct string
                if talks_about_butts:
                    #TODO: Randomize which imgur link is posted as part of the reply string using a new function
                    #comment.reply(reply_string) #reply to the comment
                    print("Replied to a comment")
                already_checked.append(comment.permalink) #add comment to already_checked
        i+=1
        print "-----------------------------------------------------------------"
    time.sleep(5) #sleep for a little bit to allow time for new comments to be made