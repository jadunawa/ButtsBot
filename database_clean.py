__author__ = 'judson'

import os, praw, sqlite3, time
from datetime import datetime
from dateutil import parser

r = praw.Reddit(user_agent='I clean buttsbot\'s database!')

path_to_script=os.path.dirname(__file__)
#print path_to_script

#connect to sqlite database
conn=sqlite3.connect(path_to_script+'/links.db')
c=conn.cursor()

#submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date
day_ago = datetime.fromtimestamp(time.time() - (48 * 60 * 60))  # find date for 24 hours ago

permas_list=c.execute("SELECT link FROM permalinks ").fetchall()

before_length=len(permas_list)
print "Before: "+str(len(permas_list))
i=0

#count for deleted
deleted=0

#count for undeleted in a row
consecutive_saved=0

#permas_list.reverse()

for full_link in permas_list:

    #print "Scanning "+str(i)
    link = "\""+ str(full_link)+"\""
    permalink=link[4:-4]

    #get submission from permalink
    #submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date
    #print submission_date
    #submission_date=datetime.now()

    #TODO: GET TIMESTAMP FROM DATABASE INSTEAD OF PRAW
    submission_date_NETWORKLESS=str(c.execute("SELECT timestamp FROM permalinks WHERE link='{}'".format(permalink,)).fetchone())
    sub_date_string=str(submission_date_NETWORKLESS)
    if (str(submission_date_NETWORKLESS)!="(None,)"):
        print "checking with date from database"
        #print "Large: "+sub_date_string
        sub_date_string_small=sub_date_string[3:-3]
        #print "Small: "+sub_date_string_small
        #print "Current time is: "+str(datetime.now())
        final_date=parser.parse(sub_date_string_small)
        #print "final date: "+str(final_date)
        submission_date=final_date
    else:
        submission = r.get_submission(permalink)
        submission_date=datetime.fromtimestamp(submission.created_utc)  # get submission date

    #delete comment from database
    print "checking post "+str(i)+": "+permalink
    if (int((day_ago - submission_date).days) > 2):
        #print "deleting: "+str(permalink)
        c.execute('''DELETE FROM permalinks WHERE link=(?)''',(permalink,))
        print "Deleted: "+permalink
        deleted+=1
        print "have deleted: "+str(deleted)
        #print "--------------------------------------------------------------------------------------------------------------------------"
    else: consecutive_saved+=1

    print "consecutive saved: "+str(consecutive_saved)

    conn.commit()

    if consecutive_saved==5:
        break


    i+=1
    #print submission

permas_list=c.execute("SELECT link FROM permalinks ").fetchall()
print "After: "+str(len(permas_list))