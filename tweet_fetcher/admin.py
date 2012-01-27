from django.contrib import admin
from tweet_fetcher.models import Search, User, Tweet

admin.site.register(Search)
admin.site.register(User)
admin.site.register(Tweet)
