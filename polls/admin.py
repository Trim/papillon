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

"""
Settings for administration pages
"""

from papillon.polls.models import Poll, Category
from django.contrib import admin

class PollAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ('name', 'category', 'modification_date', 'public', 'open')
    list_filter = ('public', 'open', 'category')

# register of differents database fields
admin.site.register(Category)
admin.site.register(Poll, PollAdmin)
