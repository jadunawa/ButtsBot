__author__ = 'judson'

import os, sqlite3, time, praw, sys
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta

path_to_script=os.path.dirname(__file__)
path_to_script=os.path.dirname(os.path.abspath(__file__))
#print path_to_script

#get bot password
config_file=open(path_to_script+"/buttsbot_config.txt",'r')
un_line=config_file.readline()
un_string=un_line[4:-1]
pw_line=config_file.readline()
pw_string=pw_line[4:-1]

#connect to sqlite database
conn=sqlite3.connect(path_to_script+'/links.db')
c=conn.cursor()

#log in to reddit
r = praw.Reddit(user_agent='I post butts!', client_id='_hEPIB-VEFigbg', client_secret='ttQBM_MIb56yuwH_f9Ukb4VbJ5c', username='ButtsBot', password=pw_string)

#submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date
two_days_ago = datetime.fromtimestamp(time.time() - (48 * 60 * 60))  # find date for 24 hours ago
print("2 days ago is: "+str(two_days_ago))
print("time is: "+str(datetime.fromtimestamp(time.time())))

permas_list=c.execute("SELECT link FROM permalinks ").fetchall()

before_length=len(permas_list)
print("Before: "+str(before_length))
i=1

#count for deleted
deleted=0

#count for undeleted in a row
consecutive_saved=0

#permas_list.reverse()

for full_link in permas_list:

    #print "Scanning "+str(i)
    link = "\""+ str(full_link)+"\""
    permalink=link[4:-4]
    #make full url
    permalink="/"+permalink

    #get submission from permalink
    #submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date
    #print submission_date
    #submission_date=datetime.now()

    #get timestamp from database instead of using praw to get it online
    #print("going to check perma: "+permalink)

    submission_date_NETWORKLESS=str(c.execute("SELECT timestamp FROM permalinks WHERE link='{}'".format(permalink,)).fetchone())
    sub_date_string=str(submission_date_NETWORKLESS)

    if (sub_date_string!="None"):
        print("checking with date from database")
        sub_date_string_small=sub_date_string[3:-3]
        final_date=parser.parse(sub_date_string_small)
        #print "final date: "+str(final_date)
        submission_date=final_date
    else:
        print("GOT HERE")
        submission = r.submission(url="https://reddit.com"+permalink)
        submission_date=datetime.fromtimestamp(submission.created_utc)  # get submission date

    #check to see if the post is too old
    print("submission date: "+str(submission_date))
    print("submission date: "+str(submission_date+relativedelta(years=+2000)))
    submission_date=submission_date+relativedelta(years=+2000)
    days_since_post = int((two_days_ago - submission_date).days)
    print("checking post "+str(i)+": "+permalink)
    print("Day difference: "+str(int((two_days_ago - submission_date).days)))

    if (days_since_post > 2):
        #delete comment from database
        #print "deleting: "+str(permalink)
        #c.execute('''DELETE FROM permalinks WHERE link=(?)''',(permalink,))
        print("Deleted: "+permalink)
        deleted+=1
        print("have deleted: "+str(deleted))
        consecutive_saved=0

    else: consecutive_saved+=1

    print("consecutive saved: "+str(consecutive_saved))

    conn.commit()



    i+=1
    #print submission
    print("--------------------------------------------------------------------------------------------------------------------------")

    if consecutive_saved==5:
        break


print("\n\n")
#final information printout
permas_list=c.execute("SELECT link FROM permalinks ").fetchall()
print("Before: "+str(before_length))
print("After: "+str(len(permas_list)))
print("Checked: "+str(i-1))
print("Deleted: "+str(deleted))