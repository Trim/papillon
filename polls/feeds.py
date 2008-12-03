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

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import Feed
from django.utils.translation import gettext_lazy as _

from settings import BASE_SITE
from polls.models import Poll, Vote, Voter

class VoterFeedObject:
    def __init__(self, voter):
        self.voter = voter

class PollLatestEntries(Feed):
    def get_object(self, poll_url):
        if len(poll_url) < 1:
            raise ObjectDoesNotExist
        return Poll.objects.get(base_url=poll_url[0])

    def title(self, obj):
        return _("Papillon - poll : ") + obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return BASE_SITE + "papillon/poll/" + obj.base_url

    def description(self, obj):
        return obj.description

    def item_link(self, voter):
        url = "%spapillon/poll/%s_%d" % (BASE_SITE, voter.poll.base_url,
                               time.mktime(voter.modification_date.timetuple()))
        return url

    def items(self, obj):
        voters = Voter.objects.filter(poll__id=obj.id).\
order_by('-modification_date')[:10]
        return voters