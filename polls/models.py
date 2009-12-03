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

import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from papillon.settings import DAYS_TO_LIVE

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
    base_url = models.CharField(max_length=100, help_text=_('Copy this \
address and send it to voters who want to participate to this poll'))
    admin_url = models.CharField(max_length=100,  help_text=_("Address to \
modify the current poll"))
    author_name = models.CharField(verbose_name=_("Author name"), 
       max_length=100, help_text=_("Name, firstname or nickname of the author"))
    author = models.ForeignKey(PollUser, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name=_("Poll name"),
                            help_text=_("Global name to present the poll"))
    description = models.CharField(max_length=1000,
                            verbose_name=_("Poll description"), 
                            help_text=_("Precise description of the poll"))
    category = models.ForeignKey(Category, null=True, blank=True)
    TYPE = (('P', _('Yes/No poll')),
            ('B', _('Yes/No/Maybe poll')),
            ('O', _('One choice poll')),)
    type = models.CharField(max_length=1, choices=TYPE,
                      verbose_name=_("Type of the poll"),
                      help_text=_("""Type of the poll:

 - "Yes/No poll" is the appropriate type for a simple multi-choice poll
 - "Yes/No/Maybe poll" allows voters to stay undecided
 - "One choice poll" gives only one option to choose from
"""))
    dated_choices = models.BooleanField(verbose_name=_("Choices are dates"),
        default=False, help_text=_("Check this option to choose between dates"))
    enddate = models.DateTimeField(null=True, blank=True,
verbose_name=_("Closing date"), help_text=_("Closing date for participating to \
the poll"))
    modification_date = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False,
verbose_name=_("Display the poll on main page"), help_text=_("Check this \
option to make the poll public"))
    opened_admin = models.BooleanField(default=False,
verbose_name=_("Allow users to add choices"), help_text=_("Check this option \
to open the poll to new choices submitted by users"))
    hide_choices = models.BooleanField(default=False,
verbose_name=_("Hide votes to new voters"), help_text=_("Check this option to \
hide poll results to new users"))
    open = models.BooleanField(default=True,
verbose_name=_("State of the poll"), help_text=_("Uncheck this option to close \
the poll/check the poll to reopen it"))

    def getTypeLabel(self):
        idx = [type[0] for type in self.TYPE].index(self.type)
        return Poll.TYPE[idx][1]

    def checkForErasement(self):
        '''Check if the poll has to be deleted'''
        if not DAYS_TO_LIVE:
            return
        now = datetime.datetime.now()
        dtl = datetime.timedelta(days=DAYS_TO_LIVE)
        if self.modification_date + dtl > now:
            return
        voters = Voter.objects.filter(poll=self)
        for voter in voters:
            if voter.modification_date + dtl > now:
                return
        for voter in voters:
            voter.user.delete()
            voter.delete()
        comments = Comment.objects.filter(poll=self)
        for comment in comments:
            comment.delete()
        self.delete()

    def getChoices(self):
        """
        Get choices associated to this vote"""
        return Choice.objects.filter(poll=self)

    class Admin:
        pass
    class Meta:
        ordering = ['-modification_date']
    def __unicode__(self):
        return self.name

class Comment(models.Model):
    '''Comment for a poll'''
    poll = models.ForeignKey(Poll)
    author_name = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['date']

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

    def getSum(self, balanced_poll=None):
        '''Get the sum of votes for this choice'''
        sum = 0
        for vote in Vote.objects.filter(choice=self, value__isnull=False):
            sum += vote.value
        if balanced_poll:
            return sum/2
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
