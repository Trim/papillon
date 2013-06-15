.. -*- coding: utf-8 -*-

=====================
Papillon installation
=====================

:Author: Étienne Loks
:Date: 2013-06-15
:Copyright: CC-BY 3.0

This document presents the installation of Papillon on a machine with GNU/Linux.
Instructions are given for Debian and bash but they are easy to adapt to other distribution and other shells.

.. contents::

Requirements
------------

 - `apache <http://www.apache.org/>`_ version 2.x (or another webserver)

 - `python <http://www.python.org/>`_ versions 2.6 or superior

 - `python-markdown <http://sourceforge.net/projects/python-markdown/>`_

 - `django <http://www.djangoproject.com/>`_ version 1.4

 - `django-south <http://south.aeracode.org/>`_ version 0.7

 - `gettext <http://www.gnu.org/software/gettext/>`_



The simple way to obtain theses elements is to get package from your favourite linux distribution.

For instance the packages for Debian wheezy are get with::

    $ sudo apt-get install python python-django python-django-south
    $ sudo apt-get install python-markdown gettext apache2

Otherwise refer to the sites of these applications.
Optionnal requesite:

 - `tinymce <http://tinymce.moxiecode.com/>`_: Javascript WYSIWYG Editor. If you want to use it don't forget to edit TINYMCE_URL in settings.py.

Choose an install path
----------------------

First of all you have to choose an install path::

    INSTALL_PATH=/var/local/django/

Of course you have to create it if it doesn't exist.

Getting the sources
-------------------

The last "stable" version is available in this `directory <http://www.peacefrogs.net/download/papillon/>`.

Another solution is to get it from the git repository::

    cd $INSTALL_PATH
    git clone git://www.peacefrogs.net/git/papillon
    cd papillon
    git tag -l # list tagged versions
    git checkout v0.3.1 # checkout the desired version

Install the sources
-------------------

If necessary unpack then move the sources in a directory readable to the apache user (www-data in Debian)::

    cd $INSTALL_PATH
    sudo tar xvjf /home/etienne/papillon-last.tar.bz2
    cd papillon
    sudo chown -R etienne:www-data papillon


In your Papillon application directory copy **local_settings.py.sample** to **local_settings.py**.
There is juste a few parameters to give.::

    cd $INSTALL_PATH
    cd papillon/papillon
    PAPILLON_PATH=`pwd`
    cp local_settings.py.sample local_settings.py
    vim local_settings.py

    ####
    EXTRA_URL = '' # extra_url path

    MAX_COMMENT_NB = 20 # max number of comments by poll - 0 to disable comments
    ALLOW_FRONTPAGE_POLL = False # disabled is recommanded for public instance

    (...)
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
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

If your Papillon is going to be used by many people, it is recommanded to use a "real" database like mysql or postgresql.

In the directory Papillon, put up a symbolic link to the basic styles django (change the path depending on your installation of django)::

    cd $PAPILLON_PATH
    ln -s /usr/share/pyshared/django/contrib/admin/static/admin/ static/


Database initialisation
-----------------------
In the directory Papillon simply::

    cd $PAPILLON_PATH
    ./manage.py syncdb

Answer the questions to create an administrator (administration pages can be found at: http://where_is_papillon/admin) then::

    cd $PAPILLON_PATH
    ./manage.py migrate polls

If you use sqlite (default database) give the write rights on the database file to the apache user::

    cd $PAPILLON_PATH
    chmod g+w papillon.db
    chmod g+w .

Compiling languages
-------------------

If your language is available in the locale directory of Papillon, you will just need to get it compiled. Still being in the Papillon directory, this can be done with (here, "de" stands for german. Replace it with the appropriate language code)::

    cd $PAPILLON_PATH
    django-admin compilemessages -l de

If your language is not available, feel free to create the default po files and to submit it, contributions are well appreciated. Procedure is as follows.

You first need to create the default po file (of course, replace "de" according to the language you chose to create)::

    cd $PAPILLON_PATH
    django-admin makemessages -l de

There should now be a django.po file in locale/de/LC_MESSAGES. Complete it with your translation.

Now that the translation file is completed, just compile it the same way you would have if the language file was already available.

Webserver configuration
-----------------------

Only Apache configuration is given. Papillon can probably be run on other
webserver feel free to complete this documentation.

Apache configuration
********************

Three configuration files are provided:

 - apache-modpython.conf: for installation with mod_python on extra path

 - apache-modpython-virtualhost.conf: for installation with mod_python on a virtual host

 - apache-wsgi.conf: for installation with WSGI on a virtual host

WSGI is recommanded.

Install with mod_python
+++++++++++++++++++++++

Install mod_python for apache::

    sudo apt-get install libapache2-mod-python

Copy and adapt the choosen configuration file for Papillon::

    cd $INSTALL_PATH
    sudo cp papillon/docs/conf/apache-modpython.conf /etc/apache2/sites-available/papillon
    sudo nano /etc/apache2/sites-available/papillon

Active this site, reload Apache and now your Papillon "can fly"::

    sudo a2ensite papillon
    sudo /etc/init.d/apache2 reload

Install with mod_wsgi
+++++++++++++++++++++++

Install mod_wsgi for apache::

    sudo apt-get install libapache2-mod-wsgi

Copy and adapt the apache configuration file for Papillon::

    cd $INSTALL_PATH
    sudo cp docs/conf/apache-wsgi.conf /etc/apache2/sites-available/papillon
    sudo nano /etc/apache2/sites-available/papillon

Copy and adapt the wsgi configuration file for Papillon::

    cd $INSTALL_PATH
    sudo mkdir apache
    sudo cp docs/conf/django.wsgi apache/
    sudo nano apache2/django.wsgi

Active this site, reload Apache and now your Papillon "can fly" (with WSGI wings)::

    sudo a2ensite papillon
    sudo /etc/init.d/apache2 reload


Post-installation
-----------------

To configure categories go to the administration interface at http://where_is_papillon/admin .


