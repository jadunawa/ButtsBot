__author__ = 'judson'

import os, praw, sqlite3, time
from datetime import datetime

r = praw.Reddit(user_agent='I clean databases!')

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

for full_link in permas_list:
    #print "Scanning "+str(i)
    link = "\""+ str(full_link)+"\""
    permalink=link[4:-4]

    submission = r.get_submission(permalink)
    submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date

    does_it_find_a_match=str(c.execute('''SELECT link FROM permalinks WHERE link=(?)''',(str(full_link),)))
    #if does_it_find_a_match!="None":
        #print "WE FOUND A LINK"

    #delete comment from database
    if (int((day_ago - submission_date).days) > 2):
        #print "deleting: "+str(permalink)
        c.execute('''DELETE FROM permalinks WHERE link=(?)''',(permalink,))
        #print "--------------------------------------------------------------------------------------------------------------------------"

    conn.commit()
    i+=1
    #print submission

permas_list=c.execute("SELECT link FROM permalinks ").fetchall()
print "After: "+str(len(permas_list))