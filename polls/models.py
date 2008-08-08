#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>
# This program can be distributed under the terms of the GNU GPL.
# See the file COPYING.

from django.db import models

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
    STATUS = (('A', 'Available'),
              ('D', 'Disabled'),)
    status = models.CharField(maxlength=1, choices=STATUS)
    TYPE = (('M', 'Meeting'), 
            ('P', 'Poll'),
            ('B', 'Balanced poll'),
            ('O', 'One choice poll'),)
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
    VOTE = ((-1, 'No'), 
            (0, 'Maybe'),
            (1, 'Yes'),)
    value = models.IntegerField(choices=VOTE)

