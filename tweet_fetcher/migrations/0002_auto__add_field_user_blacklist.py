# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'User.blacklist'
        db.add_column('tweet_fetcher_user', 'blacklist', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'User.blacklist'
        db.delete_column('tweet_fetcher_user', 'blacklist')


    models = {
        'tweet_fetcher.retweet': {
            'Meta': {'object_name': 'Retweet'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_retweet'", 'to': "orm['tweet_fetcher.Tweet']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tweet_retweet'", 'to': "orm['tweet_fetcher.User']"})
        },
        'tweet_fetcher.search': {
            'Meta': {'object_name': 'Search'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'token_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'token_secret': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'tweet_fetcher.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'last_retweet': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'retweet': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_retweet'", 'symmetrical': 'False', 'through': "orm['tweet_fetcher.Retweet']", 'to': "orm['tweet_fetcher.User']"}),
            'search': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tweet_fetcher.Search']", 'symmetrical': 'False'}),
            'twitter_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tweet_fetcher.User']"})
        },
        'tweet_fetcher.user': {
            'Meta': {'object_name': 'User'},
            'blacklist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'personal_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'twitter_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['tweet_fetcher']
