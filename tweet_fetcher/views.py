from django.views.generic.base import View
from models import Tweet

from datetime import datetime, timedelta
from django.http import HttpResponse

class StatusView(View):
    
    def get(self, request, *args, **kwargs):
        status = Tweet.objects.filter(date__gte=datetime.now() + timedelta(days=-1)).count() > 0
        return HttpResponse("%s" % 1 if status else 0)