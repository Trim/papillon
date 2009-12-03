#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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
Forms management
'''

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

from papillon.polls.models import Poll, Category

class PollForm(forms.ModelForm):
    name = forms.CharField(label=_("Poll name"), max_length=200,
                  help_text=_("Global name to present the poll"))
    description = forms.CharField(label=_("Poll description"), max_length=200,
                  help_text=_("Precise description of the poll"), 
                  widget=forms.widgets.Textarea())

class CreatePollForm(PollForm):
    class Meta:
        model = Poll
        exclude = ['base_url', 'admin_url', 'open', 'author', 'enddate', 
                    'public', 'opened_admin', 'hide_choices']
        if not Category.objects.all():
            exclude.append('category')
    type = forms.ChoiceField(label=_("Type of the poll"),
               choices=Poll.TYPE, help_text=_("""Type of the poll:

 - "Yes/No poll" is the appropriate type for a simple multi-choice poll
 - "Yes/No/Maybe poll" allows voters to stay undecided
 - "One choice poll" gives only one option to choose from
"""))
    """
    dated_choices = forms.BooleanField(
             required=False, help_text=_("Check this option to choose between \
dates"))"""
    if Category.objects.all():
        category = forms.ChoiceField(label="", help_text="Category of the poll",
               choices=[(cat.id, cat.name) for cat in Category.objects.all()])

class AdminPollForm(PollForm):
    class Meta:
        model = Poll
        exclude = ['author', 'author_name', 'base_url', 'admin_url',
                   'dated_choices', 'type']
        if not Category.objects.all():
            exclude.append('category')
    open = forms.BooleanField(label=_("State of the poll"), 
             required=False, help_text=_("Uncheck this option to close the \
poll/check the poll to reopen it"))
    public = forms.BooleanField(label=_("Display the poll on main page"), 
             required=False, help_text=_("Check this option to make the poll \
public"))
    opened_admin = forms.BooleanField(label=_("Allow users to add choices"), 
             required=False, help_text=_("Check this option to open the poll to\
 new choices submitted by users"))
    hide_choices = forms.BooleanField(label=_("Hide votes to new voters"), 
             required=False, help_text=_("Check this option to hide poll \
results to new users"))
    enddate = forms.DateField(label=_("Closing date"), 
required=False, help_text=_("Closing date for participating to the poll"))

