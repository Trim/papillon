.. -*- coding: utf-8 -*-

=====================
Papillon installation
=====================

:Author: Étienne Loks
:Date: 2011-10-25
:Copyright: CC-BY 3.0

This document presents the installation of Ishtar on a machine with GNU/Linux.
Instruction are given for Debian but they are easy to adapt to other distribution.

.. contents::

Requirements
------------

 - `apache <http://www.apache.org/>`_ version 2.x (or another webserver)

 - `python <http://www.python.org/>`_ versions 2.6 or superior

 - `python-markdown <http://sourceforge.net/projects/python-markdown/>`_

 - `django <http://www.djangoproject.com/>`_ version 1.2

 - `django-south <http://south.aeracode.org/>`_ version 0.7

 - `gettext <http://www.gnu.org/software/gettext/>`_



The simple way to obtain theses elements is to get package from your favourite linux distribution.

For instance the packages for Debian squeeze are get with::

    $ sudo apt-get install python python-django python-django-south
    $ sudo apt-get install python-markdown gettext apache2 libapache2-mod-python

Otherwise refer to the sites of these applications.
Optionnal requesite:

 - `tinymce <http://tinymce.moxiecode.com/>`_: Javascript WYSIWYG Editor. If you want to use it don't forget to edit TINYMCE_URL in settings.py.


Getting the sources
-------------------

The last "stable" version is available in this `directory <http://www.peacefrogs.net/download/>`.

Another solution is to get it from the git repository (inside /var/local/django/ if you want to strictly follow this HOWTO)::

    $ git clone git://www.peacefrogs.net/git/papillon
    $ cd papillon
    $ git tag -l # list tagged versions
    $ git checkout v0.3 # checkout the desired version

Install the sources
-------------------

If necessary unpack then move the sources in a directory readable to the apache user (www-data in Debian)::

    sudo mkdir /var/local/django
    cd /var/local/django
    sudo tar xvjf /home/etienne/papillon-last.tar.bz2
    cd /var/local/django/papillon
    sudo chown -R etienne:www-data papillon


In your Papillon application directory create settings.py to fit to your configuration.
A base template is provided (settings.py.tpl). The main parameters to change are pointed here::

    $ cd /var/local/papillon/papillon/
    $ PAPILLON_DIR=`pwd`
    $ cp settings.py.tpl settings.py
    $ nano settings.py
    ####
    EXTRA_URL = '' # extra_url path

    MAX_COMMENT_NB = 20 # max number of comments by poll - 0 to disable comments
    ALLOW_FRONTPAGE_POLL = False # disabled is recommanded for public instance

    (...)
    DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'papillon',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
    }
    SECRET_KEY = 'replace_this_with_something_else'
    # if you have set an EXTRA_URL set the full path
    MEDIA_URL = '/static/'
    # if you have set an EXTRA_URL set the full path
    ADMIN_MEDIA_PREFIX = '/media/'
    (...)

If your papillon is going to be used by many people, it is recommanded to use a "real" database like mysql or postgresql.

In the directory Papillon, put up a symbolic link to the basic styles django (change the path depending on your installation of django)::

    $ ln -s /usr/share/python-support/python-django/django/contrib/admin/media/ .


Database initialisation
-----------------------
In the directory Papillon simply::

    $ ./manage.py syncdb

Answer the questions to create an administrator (administration pages can be found at: http://where_is_papillon/admin) then::

    $ ./manage.py migrate polls

If you use sqlite (default database) give the write rights on the database file to the apache user::

    $ chmod g+w papillon.db
    $ chmod g+w .

Compiling languages
-------------------

If your language is available in the locale directory of Papillon, you will just need to get it compiled. Still being in the papillon directory, this can be done with (here, "de" stands for german. Replace it with the appropriate language code)::

    django-admin compilemessages -l de

If your language is not available, feel free to create the default po files and to submit it, contributions are well appreciated. Procedure is as follows.

You first need to create the default po file (of course, replace "de" according to the language you chose to create)::

    django-admin makemessages -l de

There should now be a django.po file in locale/de/LC_MESSAGES. Complete it with your translation.

Now that the translation file is completed, just compile it the same way you would have if the language file was already available.

Webserver configuration
-----------------------

Only Apache configuration is given. Papillon can probably be run on other
webserver feel free to complete this documentation.

Apache mod_python configuration
*******************************

Create and edit a configuration file for Papillon::

    sudo vim /etc/apache2/sites-available/papillon


Insert Apache directives for your installation::

    # part of the address after the root of your site: EXTRA_URL
    <Location "/papillon/">
    # directory path to the father of the installation of Papillon
    PythonPath "['/var/local/django/papillon/'] + sys.path"
    SetHandler python-program
    PythonHandler django.core.handlers.modpython
    SetEnv DJANGO_SETTINGS_MODULE papillon.settings
    # set it to on or off if in test or production environment
    PythonDebug On
    # put differents interpreter names if you deploy several Papillon
    PythonInterpreter papillon
    </Location>

Or if you want to use a virtual domain::

    <VirtualHost *:80>
    ServerName papillon.youdomain.net
    # directory path to the father of the installation of Papillon
    PythonPath "['/var/local/django/papillon/'] + sys.path"
    SetHandler python-program
    PythonHandler django.core.handlers.modpython
    SetEnv DJANGO_SETTINGS_MODULE papillon.settings
    # set it to on or off if in test or production environment
    PythonDebug On
    # put differents interpreter names if you deploy several Papillon
    PythonInterpreter papillon
    </VirtualHost>

Active this site, reload Apache and now your Papillon "can fly"::

    sudo a2ensite papillon
    sudo /etc/init.d/apache2 reload


Post-installation
-----------------

To configure categories go to the administration interface at http://where_is_papillon/admin .


