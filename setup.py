#!/usr/bin/env python
from setuptools import setup, find_packages

import tweet_fetcher

CLASSIFIERS = [
    'Intended Audience :: Developers',    
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python'    
]

KEYWORDS = 'django twitter tweet fetcher'

setup(name = 'tweet_fetcher',
    version = tweet_fetcher.__version__,
    description = """fetch tweets""",
    author = tweet_fetcher.__author__,
    url = "https://github.com/oxys-net/django-tweet-fetcher",
    packages = find_packages(),
    classifiers = CLASSIFIERS,
    keywords = KEYWORDS,
    zip_safe = True,
    install_requires = ["oauth2>=1.5.211", "PIL>=1.1.7"]
)