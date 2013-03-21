# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Search'
        db.create_table('tweet_fetcher_search', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('q', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('max_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('token_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('token_secret', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('tweet_fetcher', ['Search'])

        # Adding model 'User'
        db.create_table('tweet_fetcher_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('twitter_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, db_index=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True)),
            ('personal_url', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
        ))
        db.send_create_signal('tweet_fetcher', ['User'])

        # Adding model 'Tweet'
        db.create_table('tweet_fetcher_tweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_retweet', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('twitter_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, db_index=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweet_fetcher.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('tweet_fetcher', ['Tweet'])

        # Adding M2M table for field search on 'Tweet'
        db.create_table('tweet_fetcher_tweet_search', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tweet', models.ForeignKey(orm['tweet_fetcher.tweet'], null=False)),
            ('search', models.ForeignKey(orm['tweet_fetcher.search'], null=False))
        ))
        db.create_unique('tweet_fetcher_tweet_search', ['tweet_id', 'search_id'])

        # Adding model 'Retweet'
        db.create_table('tweet_fetcher_retweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tweet_retweet', to=orm['tweet_fetcher.User'])),
            ('tweet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_retweet', to=orm['tweet_fetcher.Tweet'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('tweet_fetcher', ['Retweet'])


    def backwards(self, orm):
        
        # Deleting model 'Search'
        db.delete_table('tweet_fetcher_search')

        # Deleting model 'User'
        db.delete_table('tweet_fetcher_user')

        # Deleting model 'Tweet'
        db.delete_table('tweet_fetcher_tweet')

        # Removing M2M table for field search on 'Tweet'
        db.delete_table('tweet_fetcher_tweet_search')

        # Deleting model 'Retweet'
        db.delete_table('tweet_fetcher_retweet')


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
