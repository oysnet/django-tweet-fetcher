from celery.task.base import PeriodicTask
from celery.task.schedules import crontab
from django.core import management


class FetchTweets(PeriodicTask):
    run_every = crontab(minute='*/5')
    
    def run(self, **kwargs):
        management.call_command('fetch_tweets', verbosity=0, interactive=False)
