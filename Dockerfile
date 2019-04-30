FROM python:3
ADD buttsbot_cron.py /
ADD buttsbot_config.txt /
ADD links.db /
ADD unsubscribed.txt /
RUN pip install praw
CMD [ "python", "buttsbot_cron.py" ]