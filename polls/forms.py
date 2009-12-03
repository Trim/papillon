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
from django.contrib.admin import widgets as adminwidgets

from papillon.polls.models import Poll, Category
from papillon import settings

class TextareaWidget(forms.Textarea):
    """
    Manage the edition of a text using TinyMCE
    """
    class Media:
        js = ["%stiny_mce.js" % settings.TINYMCE_URL,
              "%stextareas.js" % settings.MEDIA_URL,]


class PollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = TextareaWidget()

class CreatePollForm(PollForm):
    class Meta:
        model = Poll
        exclude = ['base_url', 'admin_url', 'open', 'author', 'enddate', 
                    'public', 'opened_admin', 'hide_choices']
        if not Category.objects.all():
            exclude.append('category')

class AdminPollForm(PollForm):
    class Meta:
        model = Poll
        exclude = ['author', 'author_name', 'base_url', 'admin_url',
                   'dated_choices', 'type']
        if not Category.objects.all():
            exclude.append('category')
    def __init__(self, *args, **kwargs):
        super(AdminPollForm, self).__init__(*args, **kwargs)
        self.fields['enddate'].widget = adminwidgets.AdminSplitDateTime()
