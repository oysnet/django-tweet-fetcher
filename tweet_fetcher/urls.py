from django.conf.urls.defaults import patterns, include, url
from views import StatusView

urlpatterns = patterns('',
    (r'^status/$', StatusView.as_view(), {}, "tweetfetcher_status_view"),
    
)
