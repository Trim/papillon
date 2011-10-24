# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('polls_category', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('polls', ['Category'])

        # Adding model 'PollUser'
        db.create_table('polls_polluser', (
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('polls', ['PollUser'])

        # Adding model 'Poll'
        db.create_table('polls_poll', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Category'], null=True, blank=True)),
            ('hide_choices', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('enddate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.PollUser'], null=True, blank=True)),
            ('open', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('admin_url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('opened_admin', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('base_url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('author_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('dated_choices', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('polls', ['Poll'])

        # Adding model 'Comment'
        db.create_table('polls_comment', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('polls', ['Comment'])

        # Adding model 'Voter'
        db.create_table('polls_voter', (
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.PollUser'])),
        ))
        db.send_create_signal('polls', ['Voter'])

        # Adding model 'Choice'
        db.create_table('polls_choice', (
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('limit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('polls', ['Choice'])

        # Adding model 'Vote'
        db.create_table('polls_vote', (
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Voter'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Choice'])),
        ))
        db.send_create_signal('polls', ['Vote'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('polls_category')

        # Deleting model 'PollUser'
        db.delete_table('polls_polluser')

        # Deleting model 'Poll'
        db.delete_table('polls_poll')

        # Deleting model 'Comment'
        db.delete_table('polls_comment')

        # Deleting model 'Voter'
        db.delete_table('polls_voter')

        # Deleting model 'Choice'
        db.delete_table('polls_choice')

        # Deleting model 'Vote'
        db.delete_table('polls_vote')
    
    
    models = {
        'polls.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"})
        },
        'polls.comment': {
            'Meta': {'object_name': 'Comment'},
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            'admin_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.PollUser']", 'null': 'True', 'blank': 'True'}),
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'base_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Category']", 'null': 'True', 'blank': 'True'}),
            'dated_choices': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'enddate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hide_choices': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'open': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'opened_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'polls.polluser': {
            'Meta': {'object_name': 'PollUser'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'polls.vote': {
            'Meta': {'object_name': 'Vote'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Choice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Voter']"})
        },
        'polls.voter': {
            'Meta': {'object_name': 'Voter'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.PollUser']"})
        }
    }
    
    complete_apps = ['polls']
