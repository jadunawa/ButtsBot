__author__ = 'Judson Dunaway-Barlow'

#Made with PRAW: https://praw.readthedocs.org/en/latest/
#Buttsbot original code at: https://github.com/jadunawa/ButtsBot

import os 
import praw
import random
import re
import sys
import sqlite3
import time
from datetime import datetime, date, timedelta

print(str(datetime.now()))

#path_to_script=os.path.dirname(__file__)
path_to_script=os.path.dirname(os.path.abspath(__file__))
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

#get unsubscribed users
unsubbed_list=[]
unsubbed_file=open(path_to_script+"/unsubscribed.txt",'r+')
for line in unsubbed_file:
    if line[-1:]=="\n":
        line=line[:-1]
    unsubbed_list.append(line)

r = praw.Reddit(user_agent='I post butts!', client_id='_hEPIB-VEFigbg', client_secret='ttQBM_MIb56yuwH_f9Ukb4VbJ5c', username='ButtsBot', password=pw_string)
#r.login(un_string, pw_string, disable_warning=True)

#TODO: Work on regex
#fuck regex
#jk regex is pretty easy lol
keywords = ['butt', 'booty', 'bootay', 'ass', 'asses', 'keyster', 'heinie', 'hiney', 'derriere', 'posterior', 'arse', 'bottom', 'tush', 'rear', 'rearend', 'rear end', 'bum', 'caboose', 'rump', 'fanny', 'glutes', 'badonkadonk', 'backside', 'anus']  # make list of words to trigger the comment reply
# TODO: Get a list of a bunch of imgur links to Astros Butts
butt_links=['Bagwell butt!](http://imgur.com/Vkx6fMI.jpg',
            #'Castro butt!](http://www.rantsports.com/mlb/files/2014/02/Jason-Castro-Houston-Astros.jpg',
            #'Lowrie butt!](http://i.imgur.com/TwTi4DT.jpg',
            #'Conger butt!](http://i.imgur.com/P5C2BGK.jpg',
            #TEMPORARY:'Carlos Lee butt!](http://i.imgur.com/G5ZzVmp.jpg',
            'McHugh butt!](http://i.imgur.com/hClbvuL.jpg',
            #TEMPORARY:'Ausmus and Berkman butt!](http://i.imgur.com/mL5TtMx.jpg',
            #'Minor Leagues Lowrie butt!](http://i.imgur.com/VTxAaqn.jpg',
            #'Kazmir butt!](http://imgur.com/ShvX5Xq.jpg',
            'Biggio butt!](http://i.imgur.com/7DlspmL.jpg',
            'Biggio butt!](http://i.imgur.com/GYwHHxV.jpg',
            'Marwin butt!](http://i.imgur.com/mqYVpy9.jpg',
            'Julia MoralASS!](http://imgur.com/SRzPWIJ.jpg',
            #'GoGo butt!](http://i.imgur.com/Xirtvvv.jpg',
            'Correa butt!](http://i.imgur.com/Y0JPeJK.jpg',
            'Altuve butt!](http://i.imgur.com/bU64HWo.jpg',
            'Biggio bobble butt!](https://i.imgur.com/I3uavEH.jpg',
            'Lance McButt!](http://i.imgur.com/tTUpRRm.jpg',
            'Marisnick butt! (photo credit: /u/Barrel-rider)](https://i.imgur.com/BerYpNo.jpg',
            'Altuve on-deck butt! (photo credit: /u/Not_a_Clue)](http://i.imgur.com/gE8M0EE.jpg',
            'A.J. Hinch butt! (photo credit: /u/thenewtestament)](http://i.imgur.com/ghZV5Lp.jpg',
            'infamous Villar butt slide!](http://i.imgur.com/mjgWAmq.gifv',
            'Nolan Ryan butt!](http://i.imgur.com/5MZt2w1.jpg',
            'Gattis butt!](http://i.imgur.com/coT3SkI.jpg',
            'El Oso Booty!](http://i.imgur.com/BXdprcQ.jpg',
            #'Doug Fister butt!](http://i.imgur.com/u6I8Rn9.jpg',
            'Ken Giles butt!](http://i.imgur.com/IJu2wI3.jpg',
            'Cy Young winning butt!](http://i.imgur.com/NTolVAP.jpg',
            'Tony Sipp butt!](http://i.imgur.com/n5opLnu.jpg',
            #'AJ Reed butt! (photo credit: /u/2to2000)](https://i.imgur.com/QjRCWGB.jpg',
            'Correa butt! (photo credit: /u/2to2000)](https://i.imgur.com/ll3q5yy.jpg',
            'Alex Bregman butt!](http://i.imgur.com/1NGFLRc.jpg',
            'Yuli Booty!](http://i.imgur.com/swrQ3mu.jpg',
            'Reddick Heinie!](http://i.imgur.com/2ynOsd5.jpg',
            'McCann tush!](http://i.imgur.com/v2cfIME.jpg',
            'Morton butt!](http://i.imgur.com/VgPHZev.jpg',
            #'Aoki flying booty!](http://i.imgur.com/sFBiP9y.jpg',
            'Finely aged Beltran posterior!](http://i.imgur.com/bqUs2c1.jpg',
            'rally starting grASShopper!](http://i.imgur.com/rIGx35e.jpg', 
            'Verlander butt!](https://i.imgur.com/72g59Sm.jpg', 
            'Verlander squats](http://i.imgur.com/NKdvCS0.jpg',
            'Verlander the Savior bump](http://i.imgur.com/cJM5ZP3.jpg',
            'pasty Reddick \'Murican speedo butt!](https://media.giphy.com/media/3ohjUQcb6m54K1zpVm/giphy.gif',
            #'Maybin butt!](http://i.imgur.com/feDCg7i.jpg',
            'Will Harris posterior!](http://i.imgur.com/bx3TXaP.jpg',
            #'Musgrove rump!](http://i.imgur.com/8s1qLyh.jpg',
            'Peacock fanny!](http://i.imgur.com/rOuXfGQ.jpg',
            #'Centeno butt! (feat. Altuve & Correa)](http://i.imgur.com/jp0mzz1.jpg',
            'Derek Fisher heinie!](http://i.imgur.com/Bkc3kdF.jpg',
            'Springer rainbow ass!](http://i.imgur.com/2ftS6GB.jpg',
            #'Gregerson butt!](http://i.imgur.com/fBcLyLP.jpg',
            #'Colin Moran caboose!](http://i.imgur.com/1wb6RK8.jpg',
            'Big Boy Feliz butt!](http://i.imgur.com/LLGekfX.jpg',
            'Troll Hair butt!](http://i.imgur.com/OPrKkW1.jpg',
            #'Liriano butt!](http://i.imgur.com/qmtHJXA.jpg'
            ]


#subreddits to check
#subreddit = r.subreddit('Astros+ButtsBot')  # get /r/Astros
subreddit = r.subreddit('ButtsBot')
#lessons learned below:
#subreddit = r.get_subreddit('Astros+Mariners') they didn't like me here either :(
#subreddit = r.get_subreddit('Astros+TexasRangers') #temporary surprise... jk I got banned :(

i = 1
new_replies=0
# go through top 30 submissions of subreddits
for submission in subreddit.hot(limit=20):
    submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date
    day_ago = datetime.fromtimestamp(time.time() - (24 * 60 * 60))  # find date for 24 hours ago
    # ignore posts over 24 hours old
    #print("Days ago: "+str((int((day_ago - submission_date).days) + 1)))
    if (int((day_ago - submission_date).days) + 1< 3):#TODO: CHANGE BACK TO 2
        print('Testing submission ', i)
        print(submission.title)
        #print(day_ago - submission_date).days
        print("Getting comments")
        submission.comments.replace_more(limit=0) # get all comments instead of just first few
        print("Got all comments")
        all_comments = submission.comments.list()  # make array of comments
        flaternized_comments = all_comments #praw.helpers.flatten_tree(all_comments)  # ignore tree structure of comments
        # Iterate through comments in the submission
        for comment in flaternized_comments:
            #print("testing comment")
            # Ignore comments that have already been checked to avoid multiple replies to the same comment
            perma=str(comment.permalink)
            #c.execute('''INSERT INTO permalinks(link, timestamp) VALUES '{}'''.format(perma+", "+str(datetime.fromtimestamp(submission.created_utc))))
            if (str(c.execute("SELECT link FROM permalinks WHERE link='{}'".format(perma)).fetchone())=="None"):
                print("Found new comment: "+str(comment))
                try:
                    print('---\nComment: ' +str(comment.body)+'\n---')
                    l_comment = str(comment.body).lower()  # make the comment lowercase
                except:
                    print('Couldn\'t print comment')
                    l_comment='' #make empty to ignore
                #talks_about_butts = any(string in l_comment for string in keywords)
                talks_about_butts=False # #boolean for talking about butts
                for keyword in keywords:
                    regex_string=r"\b"+keyword+r"i*e*s*\b"
                    search_result=re.search(regex_string, l_comment, re.IGNORECASE)
                    #print search_result
                    if(search_result):
                        talks_about_butts=True
                        print('keyword '+keyword+" worked. Comment author was "+str(comment.author))
                        print ("permalink: "+perma)
                        #print "TRUE: "+ keyword+"\ncomment: "+perma+"\nauthor:"+str(comment.author)
                # If the comment talks about butts and isn't a comment by this bot, respond with the correct string
                #TODO: check for unsubscribed users
                if talks_about_butts and str(comment.author)!="buttsbot" and str(comment.author) not in unsubbed_list:
                    print("Comment author: "+str(comment.author))
                    butt_number=random.randint(0,len(butt_links)-1)
                    full_reply="You have activated the Astros buttsbot! Here is a picture of [{}) Thanks for enjoying Astros buttocks! Go \'Stros!\n\nAny problems with this bot? Suggestions for more butts? Please send me a message or visit /r/ButtsBot!".format(butt_links[butt_number])
                    comment.reply(full_reply) #reply to the comment
                    comment.upvote() #upvote the comment
                    print("Replied to a comment: " +str(comment.permalink))
                    new_replies+=1
                c.execute('''INSERT INTO permalinks(link, timestamp) VALUES (?,?)''',(perma, datetime.fromtimestamp((submission.created_utc))))
                #c.execute('''INSERT INTO permalinks(timestamp) VALUES (?)''',(datetime.fromtimestamp(submission.created_utc),))
                conn.commit()
        print("-----------------------------------------------------------------")
    i += 1
print('Replied to '+str(new_replies)+' comments')
