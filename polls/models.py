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

'''
Models management
'''

from django.db import models
from django.utils.translation import gettext_lazy as _

class PollUser(models.Model):
    name = models.CharField(maxlength=100)
    email = models.CharField(maxlength=100)
    password = models.CharField(maxlength=100)

class Poll(models.Model):
    name = models.CharField(maxlength=200)
    description = models.CharField(maxlength=1000)
    author = models.ForeignKey(PollUser)
    base_url = models.CharField(maxlength=100)
    admin_url = models.CharField(maxlength=100)
    STATUS = (('A', _('Available')),
              ('D', _('Disabled')),)
    status = models.CharField(maxlength=1, choices=STATUS)
    TYPE = (('M', _('Meeting')),
            ('P', _('Poll')),
            ('B', _('Balanced poll')),
            ('O', _('One choice poll')),)
    type = models.CharField(maxlength=1, choices=TYPE)

    def getTypeLabel(self):
        idx = [type[0] for type in self.TYPE].index(self.type)
        return Poll.TYPE[idx][1]

    class Admin:
        pass

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    name = models.CharField(maxlength=200)
    order = models.IntegerField()
    class Admin:
        pass

class Vote(models.Model):
    voter = models.ForeignKey(PollUser)
    choice = models.ForeignKey(Choice)
    VOTE = ((-1, _('No')),
            (0, _('Maybe')),
            (1, _('Yes')),)
    value = models.IntegerField(choices=VOTE)

