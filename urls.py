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

from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from polls.feeds import PollLatestEntries

feeds = {
    'poll': PollLatestEntries,
}

urlpatterns = patterns('',
     (r'^papillon/admin/doc/', include('django.contrib.admindocs.urls')),
     (r'^papillon/admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
     (r'^papillon/admin/(.*)', admin.site.root),
     (r'^papillon/$', 'papillon.polls.views.index'),
     (r'^papillon/create$', 'papillon.polls.views.create'),
     (r'^papillon/edit/(?P<admin_url>\w+)/$',
            'papillon.polls.views.edit'),
     (r'^papillon/editChoicesAdmin/(?P<admin_url>\w+)/$',
            'papillon.polls.views.editChoicesAdmin'),
     (r'^papillon/editChoicesUser/(?P<poll_url>\w+)/$',
            'papillon.polls.views.editChoicesUser'),
     (r'^papillon/category/(?P<category_id>\w+)/$',
            'papillon.polls.views.category'),
     (r'^papillon/poll/(?P<poll_url>\w+)/$', 'papillon.polls.views.poll'),
     (r'^papillon/poll/(?P<poll_url>\w+)/vote$', 'papillon.polls.views.poll'),
     (r'^papillon/feeds/(?P<url>.*)$',
                 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
     (r'^papillon/static/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': 'static/'}),
     (r'^papillon/media/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': 'media/'}),
     (r'^papillon/tinymce/', include('tinymce.urls')),
)
