-----
About
-----

Tweets fetcher

------------
Installation
------------

To install the latest stable version::

	pip install -e git+https://github.com/oxys-net/django-tweet-fetcher#egg=django-tweet-fetcher


You will need to include ``tweet_fetcher`` in your ``INSTALLED_APPS``::

	INSTALLED_APPS = (
	    ...
	    'tweet_fetcher',            
	)

Configure oauth access in settings.py
	
	...
	
	TWITTER_CONSUMER_KEY = "..."
	TWITTER_CONSUMER_SECRET = "..." 
