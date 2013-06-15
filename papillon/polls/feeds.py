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

import time

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from papillon.polls.models import Poll, Vote, Voter


class PollLatestEntries(Feed):
    def get_object(self, request, poll_url):
        self.request = request
        if len(poll_url) < 1:
            raise ObjectDoesNotExist
        return Poll.objects.get(base_url=poll_url)

    def title(self, obj):
        return _("Papillon - poll : ") + obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        uri = self.request.build_absolute_uri(reverse('poll',
                                                      args=[obj.base_url]))
        return uri

    def description(self, obj):
        return mark_safe(obj.description)

    def item_link(self, voter):
        url = reverse('poll',  args=[voter.poll.base_url])
        url = self.request.build_absolute_uri(reverse('poll',
                                                    args=[voter.poll.base_url]))
        url = "%s_%d" % (url[:-1], # dirty...
                         time.mktime(voter.modification_date.timetuple()))
        return url

    def items(self, obj):
        voters = Voter.objects.filter(poll=obj
                    ).order_by('-modification_date')[:10]
        return voters
