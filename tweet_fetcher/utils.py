import urllib
from httplib2 import Http
from django.utils import simplejson
import oauth2 as oauth
from django.conf import settings
from simplejson.decoder import JSONDecodeError

class RateLimitError(Exception):
    pass

def search( token_key=None, token_secret=None, **kwargs):
    
    kwargs['count'] = 100
    kwargs['include_entities'] = 1
    
    kwargs['q'] += " -filter:retweets"
    
    if kwargs.get('since_id', None) is None:
        del kwargs['since_id']
    
    results = []
    
    next_page= "?" + urllib.urlencode(kwargs)
    
    max_id = None
    consumer = oauth.Consumer(key=getattr(settings, 'TWITTER_CONSUMER_KEY'), secret=getattr(settings, 'TWITTER_CONSUMER_SECRET'))
    token = oauth.Token(key=token_key, secret=token_secret)
    client = oauth.Client(consumer, token)
    
    while next_page is not None:
    
        search_url = "https://api.twitter.com/1.1/search/tweets.json" + next_page
        #resp, content = Http().request(search_url, "GET")
        resp, content = client.request(search_url, "GET")
        
        if int(resp.status) == 400 and int(resp['x-ratelimit-remaining']) == 0:
            raise RateLimitError()
        
        _tmp_res = simplejson.loads(content.decode('utf-8'))
        if max_id is None:
            max_id = _tmp_res['search_metadata']['max_id_str']
        
        next_page = _tmp_res.get('next_page', None)
        
        results.extend(_tmp_res['statuses'])
    
    
    return max_id, results
    
    
    
def get_retweet(twitter_id, token_key, token_secret):
    
    
    consumer = oauth.Consumer(key=getattr(settings, 'TWITTER_CONSUMER_KEY'), secret=getattr(settings, 'TWITTER_CONSUMER_SECRET'))
    token = oauth.Token(key=token_key, secret=token_secret)
    client = oauth.Client(consumer, token)
    
    resp, content = client.request("https://api.twitter.com/1.1/statuses/retweets/%s.json" % twitter_id, "GET")
    if int(resp.status) == 400 and int(resp['x-ratelimit-remaining']) == 0:
        raise RateLimitError()
    elif int(resp.status) != 200:
        return []
    try:
        return simplejson.loads(content.decode('utf-8'))
    except JSONDecodeError:
        return []