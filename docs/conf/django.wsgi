import os, sys
sys.path.append('/var/local/django/papillon/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'papillon.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
