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

print len(permas_list)

#for link in permas_list:
for i in range(0,10):
    full_link=permas_list[i]
    link = "\""+ str(full_link)+"\""
    permalink=link[4:-4]

    submission = r.get_submission(permalink)
    submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date

    does_it_find_a_match=str(c.execute('''SELECT link FROM permalinks WHERE link=(?)''',(str(full_link),)))
    if does_it_find_a_match!="None":
        print "WE FOUND A LINK"

    if (int((day_ago - submission_date).days) > 2):
        #delete comment
        print "got to deleting link"
        print "deleting: "+str(permalink)
        c.execute('''DELETE FROM permalinks WHERE link=(?)''',(permalink,))

    #print submission

    print "--------------------------------------------------------------------------------------------------------------------------"

#if post is too old, delete comment?