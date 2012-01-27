from django.db import models
from StringIO import StringIO
import urllib2
from PIL import Image
import uuid
from django.core.files.base import ContentFile

class Search(models.Model):
    q = models.CharField(max_length=255)    
    active = models.BooleanField(default=True)
    max_id = models.BigIntegerField(null=True, blank=True)
    
    token_key = models.CharField(max_length=255)
    token_secret = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.q
    
class User(models.Model):
    twitter_id = models.BigIntegerField(unique=True, db_index=True)
    image = models.FileField(upload_to="twitter/%Y/%m", null=True)
    image_url = models.URLField(max_length=1024, null=True)
    personal_url = models.URLField( max_length=1024, null=True)
    name = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    language = models.CharField(max_length=2, null=True)
    
    def __unicode__(self):
        return u"%s - %s (%s)" (self.pk, self.name, self.twitter_id)
    
    def set_image(self, url):
        
        if self.image_url == url:
            return
        
        input_file = StringIO(urllib2.urlopen(url).read())
        output_file = StringIO()
        img = Image.open(input_file)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_file, "PNG")
        self.image.save(str(uuid.uuid4()) + ".png", ContentFile(output_file.getvalue()), save=False)
        self.image_url = url

class Tweet(models.Model):
    
    last_retweet = models.DateTimeField(null=True)
    
    twitter_id = models.BigIntegerField(unique=True, db_index=True)
    
    search = models.ManyToManyField(Search)
    
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    retweet = models.ManyToManyField(User,through= 'Retweet', related_name="users_retweet")
    date = models.DateTimeField()
    data = models.TextField(help_text='Raw tweet data for future')
    language = models.CharField(max_length=2)
    
    def __unicode__(self):
        return u"%s - %s... (%s, %s)" (self.pk, self.message[:30], self.twitter_id, self.search)

class Retweet(models.Model):
    user = models.ForeignKey(User, related_name="tweet_retweet")
    tweet = models.ForeignKey(Tweet, related_name="user_retweet")
    date = models.DateTimeField()
