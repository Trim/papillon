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

from datetime import datetime

from django import forms
from django.contrib.admin import widgets as adminwidgets
from django.utils.translation import gettext_lazy as _

from papillon.polls.models import Poll, Category, Choice
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

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('name', 'limit', 'poll', 'order')
    def __init__(self, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['poll'].widget = forms.HiddenInput()
        self.fields['order'].widget = forms.HiddenInput()

class DatedChoiceForm(ChoiceForm):
    def __init__(self, *args, **kwargs):
        super(DatedChoiceForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = adminwidgets.AdminSplitDateTime()

    def clean_name(self):
        try:
            poll_id = self.data['poll']
            poll = Poll.objects.get(id=int(poll_id))
        except (ValueError, Poll.DoesNotExist):
            raise forms.ValidationError(_('Invalid poll'))
        data = self.cleaned_data['name']
        if poll.dated_choices:
            # management of dates fields
            if data.startswith('[') and data.endswith(']') and "'" in data:
                datas = data.split("'")
                try:
                    assert len(datas) == 5
                    time = datas[3]
                    if not time:
                        time = '00:00:00'
                    date = "%s %s" % (datas[1], time)
                    datetime.strptime(date, '%Y-%m-%d %H:%M:%S') 
                    data = date
                except (ValueError, AssertionError):
                    raise forms.ValidationError(_('Invalid date format: \
YYYY-MM-DD HH:MM:SS'))
        return data

    def clean_limit(self):
        """
        data = eval(self.cleaned_data['name'])
        
                            new_limit = int(request.POST[key])
                            sum = choice.getSum()
                            if new_limit < sum:
                                response_dct['error'] = _("You cannot lower \
%(name)s's limit to this number : there is currently %(sum)d votes for this \
choice.") % {'name':choice.name, 'sum':sum}
                            else:
                                choice.limit = new_limit
                                choice.save()
"""
        pass
