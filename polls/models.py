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

'''
Models management
'''

from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __unicode__(self):
        return self.name

class PollUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    modification_date = models.DateTimeField(auto_now=True)

class Poll(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(PollUser)
    category = models.ForeignKey(Category, null=True, blank=True)
    enddate = models.DateTimeField(null=True, blank=True)
    base_url = models.CharField(max_length=100)
    admin_url = models.CharField(max_length=100)
    modification_date = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False)
    open = models.BooleanField(default=True)
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
    def __unicode__(self):
        return self.name

class Voter(models.Model):
    user = models.ForeignKey(PollUser)
    poll = models.ForeignKey(Poll)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['creation_date']
    def __unicode__(self):
        return _("Vote from %(user)s") % {'user':self.user.name}
    def getVotes(self, choice_ids):
        '''Get votes for a subset of choices
        '''
        query = Vote.objects.filter(voter=self)
        query = query.extra(where=['choice_id IN (%s)' \
                     % ",".join([str(choice_id) for choice_id in choice_ids])])
        return list(query.order_by('choice'))

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    name = models.CharField(max_length=200)
    order = models.IntegerField()
    limit = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    class Admin:
        pass
    class Meta:
        ordering = ['order']

    def getSum(self):
        '''Get the sum of votes for this choice'''
        sum = 0
        for vote in Vote.objects.filter(choice=self):
            sum += vote.value
        return sum

    def changeOrder(self, idx=1):
        '''
        Change a choice in the list
        '''
        if (self.order + idx) < 0:
            return
        choices = Choice.objects.filter(poll=self.poll)
        if self.order + idx > len(choices):
            return
        new_order = self.order + idx
        for choice in choices:
            if choice == self:
                continue
            if idx < 0 and choice.order < self.order \
               and choice.order >= new_order:
               choice.order += 1
               choice.save()
            if idx > 0 and choice.order > self.order \
               and choice.order <= new_order:
               choice.order -= 1
               choice.save()
        self.order = new_order
        self.save()

class Vote(models.Model):
    voter = models.ForeignKey(Voter)
    choice = models.ForeignKey(Choice)
    VOTE = ((1, (_('Yes'),  _('Yes'))),
            (0, (_('No'), _('Maybe')), ),
            (-1, (_('No'), _('No'))),)
    value = models.IntegerField(choices=VOTE, blank=True, null=True)