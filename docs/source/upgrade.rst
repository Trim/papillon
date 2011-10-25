.. -*- coding: utf-8 -*-

=======
Upgrade
=======

:Author: Étienne Loks
:Date: 2011-10-25
:Copyright: CC-BY 3.0

This document presents the upgrade from one version of Papillon to another.
Instructions are given for Debian and bash but they are easy to adapt to other distribution and other shells.

From version 0.2 (and prior) to 0.3
-----------------------------------

First of all copy the installation path, the config files and your database.
Then you'll be able to rollback if there is any problem.

Disable your installation in Apache
***********************************
::

    $ sudo a2dissite papillon
    $ sudo /etc/init.d/apache2 reload

Upgrade sources
***************

Get the new sources. Extract the tarball (from the download `directory <http://www.peacefrogs.net/download/>`_) or clone the git repository in a temporary directory::

    $ cd /tmp/
    $ git clone git://www.peacefrogs.net/git/papillon
    $ cd papillon
    $ git tag -l # list tagged versions
    $ git checkout v0.3.0 # checkout the desired version

Copy updated files to your installation (be careful to put trailing slash)::

    $ PAPILLON_PATH=/var/local/django/papillon/
    $ sudo rsync -raP /tmp/papillon/ $PAPILLON_PATH

As the Git is now used you can remove (if any) Subversion directory in your new installation::

    $ cd $PAPILLON_PATH
    $ sudo find . -name ".svn" -exec rm -rf {} \;

New dependencies
****************

In order to simplify future database evolution `django-south <http://south.aeracode.org/>`_ is now used. To install it on a debian Squeeze::

    $ sudo aptitude install python-django-south


"settings.py" changes
*********************

Many changes have to be made in settings.py.

Change any occurence of ROOT_PATH to PROJECT_PATH::

    $ cd $PAPILLON_PATH
    $ sed -i 's/ROOT_PATH/PROJECT_PATH/g' papillon/settings.py

Change the manualy set definition of the project path by the lines::

    import os.path
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

Be careful: PROJECT_PATH has no trailing slash. So for every variable
using PROJECT_PATH don't forget (if necessary) to add a slash.

For instance if you have::

    TEMPLATE_DIRS = (
        PROJECT_PATH + 'templates',
    )

Change it to::

    TEMPLATE_DIRS = (
        PROJECT_PATH + '/templates',
    )

Migrate to new version of db configuration. The lines::

    DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    DATABASE_NAME = PROJECT_PATH + 'papillon.db'             # Or path to database file if using sqlite3.
    DATABASE_USER = ''             # Not used with sqlite3.
    DATABASE_PASSWORD = ''         # Not used with sqlite3.
    DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

Become::

    DATABASES = {
        'default': {
            'ENGINE': 'sqlite3',                        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': PROJECT_PATH + 'papillon.db',   # Or path to database file if using sqlite3.
            'USER': '',                             # Not used with sqlite3.
            'PASSWORD': '',                         # Not used with sqlite3.
            'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
        }
    }

Add (and adapt) the lines::

    MAX_COMMENT_NB = 20 # max number of comments by poll - 0 to disable comments
    ALLOW_FRONTPAGE_POLL = False # disabled is recommanded for public instance

You can now remove SERVER_URL and BASE_SITE variables.
You have to change MEDIA_URL and ADMIN_MEDIA_PREFIX. If there is no EXTRA_URL and you want to keep it managed by Django, you have to change them to::

    MEDIA_URL = '/static/'
    ADMIN_MEDIA_PREFIX = '/media/'

Otherwise set the full URL.

Add South to the list of installed applications (before papillon.polls)::

    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'south',
    'papillon.polls',
    )


Update database
***************
::

    $ cd $PAPILLON_PATH
    $ cd papillon
    $ ./manage.py syncdb
    $ ./manage.py migrate polls --fake


Regeneration of translations
****************************
::

    $ cd $PAPILLON_PATH
    $ cd papillon
    $ ./manage.py compilemessages -l fr

Enable your new installation in Apache
**************************************
::

    $ sudo a2ensite papillon
    $ sudo /etc/init.d/apache2 reload
