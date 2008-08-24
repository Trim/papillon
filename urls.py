#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# See the file COPYING for details.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^papillon/admin/', include('django.contrib.admin.urls')),
     (r'^papillon/$', 'papillon.polls.views.index'),
     (r'^papillon/edit/(?P<admin_url>\w+)/$',
          'papillon.polls.views.createOrEdit'),
     (r'^papillon/poll/(?P<poll_url>\w+)/$', 'papillon.polls.views.poll'),
     (r'^papillon/poll/(?P<poll_url>\w+)/vote$', 'papillon.polls.views.poll'),
     (r'^papillon/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/local/django/papillon/static/'}),
)
