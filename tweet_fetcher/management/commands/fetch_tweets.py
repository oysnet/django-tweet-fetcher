#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tweet_fetcher.models import Search, Tweet, User, Retweet
from tweet_fetcher.utils import search, get_retweet
from django.utils import simplejson
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
import rfc822
from django.db import transaction
from django.db.models import Q

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list
    
    def handle(self, *args, **options):
        for s in Search.objects.filter(active=True):
            self._fetch_tweet(s)
            self._fetch_retweet(s)
        
    def _fetch_retweet(self,s):
        
        
        tweets = Tweet.objects.filter( Q(date__gte=datetime.now() - timedelta(days=1)) & (Q(last_retweet=None) | Q(last_retweet__lte=datetime.now() - timedelta(hours=1)))).filter(search=s).order_by('-date')[:350]
        
        if tweets.count() < 350:
            tweets = list(tweets) + list(Tweet.objects.filter(Q(date__gte=datetime.now() - timedelta(days=7)) & 
                                                         (Q(last_retweet=None) | Q(last_retweet__lte=datetime.now() - timedelta(days=1)))).filter(search=s).order_by('-date')[:350-tweets.count()])
        for tweet in tweets:
            tweet.last_retweet = datetime.now()
            
            for res in get_retweet(tweet.twitter_id,  token_key=s.token_key, token_secret=s.token_secret):
                                
                user = self._get_user(res['user']['id_str'], res['user']['name'], res['user']['screen_name'], res['user']['profile_image_url'])
                
                try:
                    Retweet.objects.get(user = user, tweet = tweet)
                    continue
                except ObjectDoesNotExist:
                    Retweet(user = user, tweet = tweet, date = datetime(*rfc822.parsedate(res['created_at'])[:6])).save()
                
            tweet.save()
    
    def _get_user(self, twitter_id, name, screen_name, profile_image):
        try:
            user = User.objects.get(twitter_id = twitter_id)
        except ObjectDoesNotExist:
            user = User(twitter_id = twitter_id)                    
            
        user.name =  name
        user.screen_name =  screen_name
        user.set_image( profile_image)
        
        user.save()
        
        return user
    
    @transaction.commit_manually
    def _fetch_tweet(self, s):
        
        # todo since_id ou stocker max_id dans Search
        try:
            
            max_id, results = search(token_key=s.token_key, token_secret=s.token_secret, q=s.q, since_id = s.max_id)
            
            for r in results:
                user = self._get_user(r['user']['id_str'], r['user']['name'], r['user']['screen_name'], r['user']['profile_image_url'])
                
                try:
                    
                    tweet = Tweet.objects.get(twitter_id = r['id_str'])
                    
                except ObjectDoesNotExist:    
                    tweet = Tweet(
                          twitter_id = r['id_str'],
                          user = user
                          )
               
                tweet.message = r['text'].strip()

                if len(r['metadata']['iso_language_code']) == 2:
                    tweet.language = r['metadata']['iso_language_code']
                tweet.date = datetime(*rfc822.parsedate(r['created_at'])[:6])
                tweet.data = simplejson.dumps(r)
                
                tweet.save()
                tweet.search.add(s)
                
            s.max_id = max_id
            s.save()
            transaction.commit()
        except:
            transaction.rollback()
            raise
        
        transaction.commit()
                
        