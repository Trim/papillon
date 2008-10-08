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
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    modification_date = models.DateTimeField(auto_now=True)

class Poll(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(PollUser)
    base_url = models.CharField(max_length=100)
    admin_url = models.CharField(max_length=100)
    modification_date = models.DateTimeField(auto_now=True)
    STATUS = (('A', _('Available')),
              ('D', _('Disabled')),)
    status = models.CharField(max_length=1, choices=STATUS)
    TYPE = (('P', _('Poll')),
            ('B', _('Balanced poll')),
            ('O', _('One choice poll')),)
    #        ('M', _('Meeting')),)
    type = models.CharField(max_length=1, choices=TYPE)

    def getTypeLabel(self):
        idx = [type[0] for type in self.TYPE].index(self.type)
        return Poll.TYPE[idx][1]
    class Admin:
        pass
    class Meta:
        ordering = ['-modification_date']

class Voter(models.Model):
    user = models.ForeignKey(PollUser)
    poll = models.ForeignKey(Poll)
    creation_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['creation_date']

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    name = models.CharField(max_length=200)
    order = models.IntegerField()
    limit = models.IntegerField(null=True)
    available = models.BooleanField(default=True)
    class Admin:
        pass
    class Meta:
        ordering = ['order']

class Vote(models.Model):
    voter = models.ForeignKey(Voter)
    choice = models.ForeignKey(Choice)
    VOTE = ((1, (_('Yes'),  _('Yes'))),
            (0, (_('No'), _('Maybe')), ),
            (-1, (_('No'), _('No'))),)
    value = models.IntegerField(choices=VOTE, null=True)
