# ButtsBot
A silly bot that posts a picture of a (clothed) butt from the Astros team whenever somebody in the /r/Astros subreddit uses any of a few certain keywords in a comment.

To copy this bot, copy the config example file `buttsbot_config_example.txt` and enter the correct username and password. It must be called `buttsbot_config.txt`. You must also copy `links_example.db` into `links.db`.

The files you will want to use are:
    
    buttsbot_cron.py (main script)
    
    buttsbot_config.txt (holds username and password for your bot)
    
    links.db (holds the links from all comments checked in the past few days and their respective timestamps)
    
    database_clean.py (removes old links from the database to make checking comment permalinks faster)
