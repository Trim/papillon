#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# See the file COPYING for details.

import settings

from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()

from polls.feeds import PollLatestEntries

base = '^' + settings.EXTRA_URL
if settings.EXTRA_URL and not base.endswith('/'):
    base += '/'

urlpatterns = patterns('papillon.polls.views',
     (base + r'admin/doc/', include('django.contrib.admindocs.urls')),
     url(base + r'admin/jsi18n/$', 'django.views.i18n.javascript_catalog',
             name='admin_i18n'),
     url(base + r'^admin/', include(admin.site.urls)),
     url(base + r'$', 'index', name='index'),
     url(base + r'create/$', 'create', name='create'),
     url(base + r'edit/(?P<admin_url>\w+)/$',
            'edit', name='edit'),
     url(base + r'editChoicesAdmin/(?P<admin_url>\w+)/$',
            'editChoicesAdmin', name='edit_choices_admin'),
     url(base + r'editChoicesUser/(?P<poll_url>\w+)/$',
            'editChoicesUser', name='edit_choices_user'),
     url(base + r'category/(?P<category_id>\w+)/$',
            'category', name='category'),
     url(base + r'poll/(?P<poll_url>\w+)/$', 'poll',
            name='poll'),
     url(base + r'poll/(?P<poll_url>\w+)/vote/$', 'poll',
            name='vote'),
     url(base + r'feeds/poll/(?P<poll_url>\w+)$', PollLatestEntries(), name='feed'),
     (base + r'static/(?P<path>.*)$', 'django.views.static.serve',
                          {'document_root': settings.PROJECT_PATH + '/static'}),
     (base + r'media/(?P<path>.*)$', 'django.views.static.serve',
                          {'document_root': settings.PROJECT_PATH + '/media/'}),
)
