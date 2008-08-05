#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>
# This program can be distributed under the terms of the GNU GPL.
# See the file COPYING.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^papillon/$', 'papillon.polls.views.index'),
     (r'^papillon/edit/(?P<admin_url>\w+)/$', 'papillon.polls.views.createOrEdit'),
     (r'^papillon/poll/(?P<poll_url>\w+)/$', 'papillon.polls.views.poll'),
     (r'^papillon/poll/(?P<poll_url>\w+)/vote$', 'papillon.polls.views.poll'),
     (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/'}),
)
