#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Clean the old polls
'''

import os
import sys

# django settings path
os.environ['DJANGO_SETTINGS_MODULE'] = 'papillon.settings'

# add the parent path to sys.path
curdir = os.path.abspath(os.curdir)
sep = os.path.sep
sys.path.append(sep.join(curdir.split(sep)[:-1]))


from papillon.polls.models import Poll

for poll in Poll.objects.all():
    poll.checkForErasement()
