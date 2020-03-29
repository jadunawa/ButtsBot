__author__ = 'Judson Dunaway-Barlow'

#Made with PRAW: https://praw.readthedocs.org/en/latest/
#Buttsbot original code at: https://github.com/jadunawa/ButtsBot

import os
import praw
import random
import re
import sys
import sqlite3
import pymysql.cursors
import time
from datetime import datetime, date, timedelta

# get current time
now = datetime.now()
print('Run time: '+str(now))

path_to_script=os.path.dirname(os.path.abspath(__file__))


# connect to RDS and use the correct database ('permalinks')
db = pymysql.connect(host = 'tf-buttsbot-checked-links.cj2uoorl5ifw.us-east-1.rds.amazonaws.com', user = 'buttsbot', passwd = '8wbei3EsF^v5', port = 3306)
cur = db.cursor()
cur.execute('use permalinks')
db.commit()


# get password
# TODO: use environment variables to do this securely and not through a txt file
config_file = open(path_to_script+"/buttsbot_config.txt",'r')
un_line = config_file.readline()
un_string = un_line[4:-1]
pw_line = config_file.readline()
pw_string = pw_line[4:-1]

# login
r = praw.Reddit(user_agent='I post butts!', client_id='_hEPIB-VEFigbg', client_secret='ttQBM_MIb56yuwH_f9Ukb4VbJ5c', username='ButtsBot', password=pw_string)

# set keywords
keywords = ['butt', 'booty', 'bootay', 'ass', 'asses', 'keyster', 'heinie', 'hiney', 'derriere', 'posterior', 'arse', 'bottom', 'tush', 'rear', 'rearend', 'rear end', 'bum', 'caboose', 'rump', 'fanny', 'glutes', 'badonkadonk', 'backside', 'anus', 'tuchus', 'tushy', 'rectum', 'sphincter']  # make list of words to trigger the comment reply

# Astros butts list
butt_links_astros = ['Bagwell butt!](http://imgur.com/Vkx6fMI.jpg',
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
            #'GoGo butt!](http://i.imgur.com/Xirtvvv.jpg',
            'Correa butt!](http://i.imgur.com/Y0JPeJK.jpg',
            'Altuve butt!](http://i.imgur.com/bU64HWo.jpg',
            'Biggio bobble butt!](https://i.imgur.com/I3uavEH.jpg',
            #'Lance McButt!](http://i.imgur.com/tTUpRRm.jpg',
            'Marisnick butt! (photo credit: /u/Barrel-rider)](https://i.imgur.com/BerYpNo.jpg',
            'Altuve on-deck butt! (photo credit: /u/Not_a_Clue)](http://i.imgur.com/gE8M0EE.jpg',
            'A.J. Hinch butt! (photo credit: /u/thenewtestament)](http://i.imgur.com/ghZV5Lp.jpg',
            'infamous Villar butt slide!](http://i.imgur.com/mjgWAmq.gifv',
            'Nolan Ryan butt!](http://i.imgur.com/5MZt2w1.jpg',
            #'Gattis butt!](http://i.imgur.com/coT3SkI.jpg',
            #'El Oso Booty!](http://i.imgur.com/BXdprcQ.jpg',
            #'Doug Fister butt!](http://i.imgur.com/u6I8Rn9.jpg',
            #'Ken Giles butt!](http://i.imgur.com/IJu2wI3.jpg',
            'Cy Young winning butt!](http://i.imgur.com/NTolVAP.jpg',
            'Tony Sipp butt!](http://i.imgur.com/n5opLnu.jpg',
            #'AJ Reed butt! (photo credit: /u/2to2000)](https://i.imgur.com/QjRCWGB.jpg',
            'Correa butt! (photo credit: /u/2to2000)](https://i.imgur.com/ll3q5yy.jpg',
            'Alex Bregman butt!](http://i.imgur.com/1NGFLRc.jpg',
            'Yuli Booty!](http://i.imgur.com/swrQ3mu.jpg',
            'Reddick Heinie!](http://i.imgur.com/2ynOsd5.jpg',
            #'McCann tush!](http://i.imgur.com/v2cfIME.jpg',
            #'Morton butt!](http://i.imgur.com/VgPHZev.jpg',
            #'Aoki flying booty!](http://i.imgur.com/sFBiP9y.jpg',
            'Finely aged Beltran posterior!](http://i.imgur.com/bqUs2c1.jpg',
            'rally starting grASShopper!](http://i.imgur.com/rIGx35e.jpg',
            'Verlander butt!](https://i.imgur.com/72g59Sm.jpg',
            'Verlander squats!](http://i.imgur.com/NKdvCS0.jpg',
            'Verlander the Savior bump!](http://i.imgur.com/cJM5ZP3.jpg',
            'pasty Reddick \'Murican speedo butt!](https://media.giphy.com/media/3ohjUQcb6m54K1zpVm/giphy.gif',
            #'Maybin butt!](http://i.imgur.com/feDCg7i.jpg',
            'Will Harris posterior!](http://i.imgur.com/bx3TXaP.jpg',
            #'Musgrove rump!](http://i.imgur.com/8s1qLyh.jpg',
            'Peacock fanny!](http://i.imgur.com/rOuXfGQ.jpg',
            #'Centeno butt! (feat. Altuve & Correa)](http://i.imgur.com/jp0mzz1.jpg',
            #'Derek Fisher heinie!](http://i.imgur.com/Bkc3kdF.jpg',
            'Springer rainbow ass!](http://i.imgur.com/2ftS6GB.jpg',
            #'Gregerson butt!](http://i.imgur.com/fBcLyLP.jpg',
            #'Colin Moran caboose!](http://i.imgur.com/1wb6RK8.jpg',
            #'Big Boy Feliz butt!](http://i.imgur.com/LLGekfX.jpg',
            'Troll Hair butt!](http://i.imgur.com/OPrKkW1.jpg',
            #'Liriano butt!](http://i.imgur.com/qmtHJXA.jpg'
            'Shark Butt ooh ha ha!](http://i.imgur.com/TqW2lbj.jpg',
            'Cole train caboose!](http://i.imgur.com/2Pwaf2b.jpg',
            #'Machete ass!](http://i.imgur.com/pQHZmcU.jpg',
            'Ultra special Bregman twerking feat JV!](https://i.imgur.com/NyQ0MgB.gifv',
            'Gerrit Cole polishing a special MVP butt!](https://i.imgur.com/cm41FTF.jpg',
            '#2\'s #2!](https://i.imgur.com/wIXH0ks.jpg',
            'Orbit streaking! (photo credit: /u/AuntieMeat)](http://i.imgur.com/wyyqYaS.jpg',
            'Myles of butt! (photo credit: /u/Lukealloneword)](https://i.imgur.com/0Z4HlYw.jpg',
            'Aledmys Diaz butt! (photo credit: /u/johnnyracer24)](https://i.imgur.com/0bFDpYL.jpg'
            'Showrrea behind! (photo credit: /u/johnnyracer24)](https://i.imgur.com/onHrWZz.jpg'
            ]

# Braes butts list
butt_links = ['Folty booty!](https://i.imgur.com/He0D8zn.png',
              'Max Fried ass!](https://i.imgur.com/ULTeXCs.jpg',
              'Cole Hamels hiney!](https://i.imgur.com/vKF1rxy.jpg',
              'Luke Jackson tush!](https://i.imgur.com/2pSyPm8.jpg',
              'Marky Mark rump!](https://i.imgur.com/XZwHkWK.jpg',
              'Southpaw Sean derriere!](https://i.imgur.com/Gpm8jkb.jpg',
              'Sweet Soroka fanny!](https://i.imgur.com/UlMhvNV.jpg',
              'Tyler Flowers catching caboose!](https://i.imgur.com/6WIsnpx.jpg',
              'Albies ass!](https://i.imgur.com/3fdqiVP.jpg',
              'Camargo caboose!](https://i.imgur.com/U9paYXl.jpg',
              'Freddie fanny!](https://i.imgur.com/ao6alv5.jpg',
              'Adeiny arse!](https://i.imgur.com/791dwx3.jpg',
              'Dansby badonkadonk!](https://i.imgur.com/92i718i.jpg',
              'Acuña ass!](https://i.imgur.com/aduoctb.jpg',
              'Ender Inciarte booty!](https://i.imgur.com/KYQEdVI.jpg',
              'Markakis cakes!](https://i.imgur.com/Z1ea014.jpg',
              'Marcell Ozuna tush!](https://i.imgur.com/xqxd8r6.jpg',
              'Austin Riley butt!](https://i.imgur.com/VVCbmpn.jpg',
              'Cristian Pache backside!](https://i.imgur.com/epQvhp2.jpg']


# subreddits to check
#subreddit = r.subreddit('Astros+ButtsBot')  # get /r/Astros
subreddit = r.subreddit('ButtsBot')

#lessons learned:
#subreddit = r.get_subreddit('Astros+Mariners') they didn't like me here either :(
#subreddit = r.get_subreddit('Astros+TexasRangers') #temporary surprise... jk I got banned :(


submission_number = 1
new_replies = 0
days_to_check = 1

# go through top 30 submissions of subreddits

# find timestamp for 24 hours ago to ignore posts from before then
day_ago = datetime.fromtimestamp(time.time() - (24 * 60 * 60))
print('24 hours ago: '+str(day_ago))

for submission in subreddit.hot(limit=20):

    # get submission date
    submission_date = datetime.fromtimestamp(submission.created_utc)

    # check if the submission is within the last <days_to_check> days
    if ((now - submission_date).days < days_to_check):

        print()

        print('Analyzing submission ', submission_number)
        print('Title: '+submission.title)

        # get comments to process
        print("Getting comments")
        submission.comments.replace_more(limit=0) # get all comments instead of just first few
        print("Got all comments")
        print()

        # move all comments to flat list
        all_comments = submission.comments.list()  # make array of comments
        flaternized_comments = all_comments #praw.helpers.flatten_tree(all_comments)  # ignore tree structure of comments

        # Iterate through comments in the submission
        for comment in flaternized_comments:

            # search to see if comment has already been analyzed

            # get permalink and handle invalid results
            try:
                perma=str(comment.permalink)
            except:
                print('Couldn\'t get permalink')
                perma='INVALID'


            # build search command
            search_command = 'SELECT link FROM permalinks WHERE link="%s";'%(perma)
            # get result
            result = cur.execute(search_command)

            # permalink not invalid and permalink not already in database (which means this comment hasn't yet been analyzed)
            if ((perma!='INVALID') and (str(cur.fetchone())=="None")):

                # add permalink to the database
                add_command = 'INSERT INTO permalinks (link, datetime) VALUES ("%s","%s");'%(perma, submission_date)
                add = cur.execute(add_command)
                db.commit()


                print("Found new comment:")
                try:
                    print('---\nComment: ' +str(comment.body)+'\n---')
                    l_comment = str(comment.body).lower()  # make the comment lowercase
                except:
                    print('Couldn\'t print comment')
                    l_comment = '' #make empty to ignore


                talks_about_butts=False # boolean for talking about butts
                # go through each of the keywords and see if it's in the comment
                for keyword in keywords:
                    regex_string = r"\b"+keyword+r"i*e*s*\b" # take plurals into account, sloppily
                    search_result = re.search(regex_string, l_comment, re.IGNORECASE) # search for the keyword in the comment, ignoring case

                    # print search_result
                    if (search_result):
                        talks_about_butts = True
                        print('keyword '+keyword+" worked. Comment author was "+str(comment.author))
                        print("permalink: "+perma)
                        #print "TRUE: "+ keyword+"\ncomment: "+perma+"\nauthor:"+str(comment.author)

                # If the comment talks about butts and isn't a comment by this bot, respond with the correct string
                #TODO: check for unsubscribed users
                if (talks_about_butts and str(comment.author) != "buttsbot"):

                    print("Comment author: "+str(comment.author))

                    # create response comment
                    butt_number = random.randint(0,len(butt_links)-1) # get random butt
                    full_reply = "You have activated the Buttsbot! Here is a picture of [{}) Thanks for enjoying Braves buttocks! Go Braves!\n\nAny problems with this bot? Suggestions for more butts? Please send me a message or visit /r/ButtsBot!".format(butt_links[butt_number])

                    # reply and upvote the comment
                    try:
                        comment.reply(full_reply) #reply to the comment
                    except:
                        print("Couldn't reply to comment (comments locked?)")
                    comment.upvote() #upvote the comment

                    print("Replied to a comment: " +str(comment.permalink))
                    new_replies += 1
                    print()
                db.commit()
        print("-----------------------------------------------------------------")
    submission_number += 1
print('Replied to '+str(new_replies)+' comments')

# close database connection
db.close()
