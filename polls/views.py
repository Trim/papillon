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
Views management
'''

from random import choice as random_choice
import string
import time
from datetime import datetime

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from papillon.settings import LANGUAGES, BASE_SITE
from papillon.polls.models import Poll, PollUser, Choice, Voter, Vote, \
                                  Category, Comment
from papillon.polls.forms import CreatePollForm, AdminPollForm, ChoiceForm, \
                                 DatedChoiceForm

def getBaseResponse(request):
    """Manage basic fields for the template
    If not null the second argument returned is a redirection.
    """
    #Get the root url in order to redirect to the main page
    url = "/".join([request.META['HTTP_HOST'],
                    request.path.split('/')[1], ''])
    # setting the current language and available languages
    if 'language' in request.GET:
        if request.GET['language'] in [language[0] for language in LANGUAGES]:
            request.session['django_language'] = request.GET['language']
            return None, HttpResponseRedirect(request.path)
    languages = []
    for language_code, language_label in LANGUAGES:
        languages.append((language_code, language_label))
    return {'root_url':url, 'languages':languages}, None

def index(request):
    "Main page"
    response_dct, redirect = getBaseResponse(request)
    if redirect:
        return redirect
    response_dct['polls'] = Poll.objects.filter(public=True, category=None)
    response_dct['categories'] = Category.objects.all()
    error = ''
    if 'bad_poll' in request.GET:
        response_dct['error'] = _("The poll requested don't exist (anymore?)")
    return render_to_response('main.html', response_dct)

def category(request, category_id):
    "Page for a category"
    response_dct, redirect = getBaseResponse(request)
    if redirect:
        return redirect
    category = Category.objects.get(id=int(category_id))
    response_dct['category'] = category
    response_dct['polls'] = Poll.objects.filter(public=True, category=category)
    return render_to_response('category.html', response_dct)

def create(request):
    '''Creation of a poll.
    '''
    def genRandomURL():
        "Generation of a random url"
        url = ''
        while not url or Poll.objects.filter(base_url=url).count() or\
              Poll.objects.filter(admin_url=url).count():
            url = ''
            chars = string.letters + string.digits
            for i in xrange(6):
                url += random_choice(chars)
            url += str(int(time.time()))
        return url

    response_dct, redirect = getBaseResponse(request)

    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            poll = form.save()
            poll.admin_url = genRandomURL()
            poll.base_url = genRandomURL()
            poll.save()
            return HttpResponseRedirect('http://%seditChoicesAdmin/%s/' % (
                            response_dct['root_url'], poll.admin_url))
    else:
        form = CreatePollForm()
    response_dct['form'] = form
    return render_to_response('create.html', response_dct)

def edit(request, admin_url):
    '''Edition of a poll.
    '''
    response_dct, redirect = getBaseResponse(request)
    try:
        poll = Poll.objects.filter(admin_url=admin_url)[0]
    except IndexError:
        # if the poll don't exist redirect to the creation page
        url = response_dct['root_url']
        return HttpResponseRedirect('http://%screate' % (
                            response_dct['root_url']))
    Form = AdminPollForm

    if request.method == 'POST':
        form = Form(request.POST, instance=poll)
        if form.is_valid():
            poll = form.save()
            return HttpResponseRedirect('http://%sedit/%s/' % (
                            response_dct['root_url'], poll.admin_url))
    else:
        form = Form(instance=poll)
    response_dct['form'] = form
    response_dct['poll'] = poll
    return render_to_response('edit.html', response_dct)

def editChoicesAdmin(request, admin_url):
    response_dct, redirect = getBaseResponse(request)
    if redirect:
        return redirect
    try:
        poll = Poll.objects.filter(admin_url=admin_url)[0]
    except IndexError:
        # if the poll don't exist redirect to the main page
        url = "/".join(request.path.split('/')[:-2])
        return response_dct, HttpResponseRedirect(url)
    response_dct['poll'] = poll
    return editChoices(request, response_dct, admin=True)

def editChoicesUser(request, poll_url):
    response_dct, redirect = getBaseResponse(request)
    if redirect:
        return redirect
    try:
        poll = Poll.objects.filter(poll_url=poll_url)[0]
    except IndexError:
        poll = None
    if not poll or not poll.opened_admin:
        # if the poll don't exist redirect to the main page
        url = "/".join(request.path.split('/')[:-2])
        return HttpResponseRedirect(url)
    response_dct['poll'] = poll
    return editChoices(request, response_dct)

def editChoices(request, response_dct, admin=False):
    '''Edition of choices.
    '''
    poll = response_dct['poll']
    tpl = 'editChoicesAdmin.html'
    if not admin:
        tpl = 'editChoicesUser.html'
    Form = ChoiceForm
    if poll.dated_choices:
        Form = DatedChoiceForm
    try:
        order = Choice.objects.order_by('-order')[0].order
        order += 1
    except IndexError:
        order = 0
    form = Form(initial={'poll':poll.id, 'order':str(order)})

    if request.method == 'POST':
        # if a new choice is submitted
        if 'add' in request.POST and request.POST['poll'] == str(poll.id):
            f = Form(request.POST)
            if f.is_valid():
                choice = f.save()
                poll.reorder()
            else:
                form = f
        if admin and 'edit' in request.POST \
           and request.POST['poll'] == str(poll.id):
            try:
                choice = Choice.objects.get(id=int(request.POST['edit']))
                if choice.poll != poll:
                    raise ValueError
                f = Form(request.POST, instance=choice)
                if f.is_valid():
                    choice = f.save()
                    poll.reorder()
            except (Choice.DoesNotExist, ValueError):
                pass
        if admin:
            # check if a choice has been choosen for deletion
            for key in request.POST:
                if key.startswith('delete_') and request.POST[key]:
                    try:
                        choice = Choice.objects.get(id=int(key[len('delete_'):]))
                        if choice.poll != poll:
                            raise ValueError
                        Vote.objects.filter(choice=choice).delete()
                        choice.delete()
                    except (Choice.DoesNotExist, ValueError):
                        pass
    # check if the order of a choice has to be changed
    if admin and request.method == 'GET':
        for key in request.GET:
            try:
                current_url = request.path.split('?')[0]
                if 'up_choice' in key:
                    choice = Choice.objects.get(id=int(request.GET[key]))
                    if choice.poll != poll:
                        raise ValueError
                    choice.changeOrder(-1)
                    poll.reorder()
                    # redirect in order to avoid a change with a refresh
                    return HttpResponseRedirect(current_url)
                if 'down_choice' in key:
                    choice = Choice.objects.get(id=int(request.GET[key]))
                    if choice.poll != poll:
                        raise ValueError
                    choice.changeOrder(1)
                    poll.reorder()
                    # redirect in order to avoid a change with a refresh
                    return HttpResponseRedirect(current_url)
            except (ValueError, Choice.DoesNotExist):
                pass
    choices = Choice.objects.filter(poll=poll).order_by('order')
    for choice in choices:
        if poll.dated_choices:
            choice.name = datetime.strptime(choice.name, '%Y-%m-%d %H:%M:%S')
        choice.form = Form(instance=choice)
    response_dct['choices'] = choices
    response_dct['form_new_choice'] = form
    return render_to_response(tpl, response_dct)

def poll(request, poll_url):
    """Display a poll
    poll_url is given to identify the poll. If '_' is in the poll_url the second
    part of the url is the unix time given to highlight a particular vote
    modification
    """

    def modifyVote(request, choices):
        "Modify user's votes"
        try:
            voter = Voter.objects.filter(
                                  id=int(request.POST['voter']))[0]
        except (ValueError, IndexError):
            return
        # if no author_name is given deletion of associated votes and
        # author
        if not request.POST['author_name']:
            # verify if the author can be deleted
            delete_user = None
            if not voter.user.password:
                v = Voter.objects.filter(user=voter.user)
                if len(v) == 1 and v[0] == voter:
                    delete_user = voter.user
            for choice in choices:
                v = Vote.objects.filter(voter=voter, choice=choice)
                v.delete()
            voter.delete()
            if delete_user:
                delete_user.delete()
            return
        # update the name
        voter.user.name = request.POST['author_name']
        voter.user.save()
        # update the modification date
        voter.save()
        selected_choices = []
        # set the selected choices
        for key in request.POST:
            # modify a one choice poll
            if key == 'vote' and request.POST[key]:
                try:
                    id = int(request.POST[key])
                    vote = Vote.objects.filter(id=id)[0]
                    if vote.choice not in choices:
                        # bad vote id : the associated choice has
                        # probably been deleted
                        vote.delete()
                    else:
                        vote.value = 1
                        vote.save()
                        selected_choices.append(vote.choice)
                except (ValueError, IndexError):
                    # the vote don't exist anymore
                    pass
            # modify an existing vote
            if key.startswith('vote_') and request.POST[key]:
                try:
                    id = int(key.split('_')[1])
                    vote = Vote.objects.filter(id=id)[0]
                    if vote.choice not in choices:
                        # bad vote id : the associated choice has
                        # probably been deleted
                        vote.delete()
                    else:
                        # try if a specific value is specified in the form
                        # like in balanced poll
                        try:
                            value = int(request.POST[key])
                        except ValueError:
                            value = 1
                        vote.value = value
                        vote.save()
                        selected_choices.append(vote.choice)
                except (ValueError, IndexError):
                    # the vote don't exist anymore
                    pass
        # update non selected choices
        for choice in choices:
            if choice not in selected_choices:
                try:
                    v = Vote.objects.filter(voter=voter, choice=choice)[0]
                    v.value = 0
                except IndexError:
                    # the vote don't exist with this choice : probably
                    # a new choice
                    v = Vote(voter=voter, choice=choice, value=0)
                v.save()
    def newComment(request, poll):
        "Comment the poll"
        if 'comment_author' not in request.POST \
           or not request.POST['comment_author'] \
           or not request.POST['comment']:
            return
        c = Comment(poll=poll, author_name=request.POST['comment_author'],
                    text=request.POST['comment'])
        c.save()

    def newVote(request, choices):
        "Create new votes"
        if not request.POST['author_name']:
            return
        author = PollUser(name=request.POST['author_name'])
        author.save()
        voter = Voter(user=author, poll=poll)
        voter.save()
        selected_choices = []

        # set the selected choices
        for key in request.POST:
            # standard vote
            if key.startswith('choice_') and request.POST[key]:
                try:
                    id = int(key.split('_')[1])
                    choice = Choice.objects.filter(id=id)[0]
                    if choice not in choices:
                        raise ValueError
                    # try if a specific value is specified in the form
                    # like in balanced poll
                    try:
                        value = int(request.POST[key])
                    except ValueError:
                        value = 1
                    v = Vote(voter=voter, choice=choice, value=value)
                    v.save()
                    selected_choices.append(choice)
                except (ValueError, IndexError):
                    # bad choice id : the choice has probably been deleted
                    pass
            # one choice vote
            if key == 'choice' and request.POST[key]:
                try:
                    id = int(request.POST[key])
                    choice = Choice.objects.filter(id=id)[0]
                    if choice not in choices:
                        raise ValueError
                    v = Vote(voter=voter, choice=choice, value=1)
                    v.save()
                    selected_choices.append(choice)
                except (ValueError, IndexError):
                    # bad choice id : the choice has probably been deleted
                    pass
        # set non selected choices
        for choice in choices:
            if choice not in selected_choices:
                v = Vote(voter=voter, choice=choice, value=0)
                v.save()
        # results can now be displayed
        request.session['knowned_vote_' + poll.base_url] = 1
    response_dct, redirect = getBaseResponse(request)
    if redirect:
        return redirect
    highlight_vote_date = None
    if '_' in poll_url:
        url_spl = poll_url.split('_')
        if len(url_spl) == 2:
            poll_url, highlight_vote_date = url_spl
            try:
                highlight_vote_date = int(highlight_vote_date)
            except ValueError:
                highlight_vote_date = None
    try:
        poll = Poll.objects.filter(base_url=poll_url)[0]
    except IndexError:
        poll = None
    choices = list(Choice.objects.filter(poll=poll))
    # if the poll don't exist or if it has no choices the user is
    # redirected to the main page
    if not choices or not poll:
        url = "/".join(request.path.split('/')[:-3])
        url += "/?bad_poll=1"
        return HttpResponseRedirect(url)

    # a vote is submitted
    if 'author_name' in request.POST and poll.open:
        if 'voter' in request.POST:
            # modification of an old vote
            modifyVote(request, choices)
        else:
            newVote(request, choices)
        # update the modification date of the poll
        poll.save()
    if 'comment' in request.POST and poll.open:
        # comment posted
        newComment(request, poll)

    # 'voter' is in request.GET when the edit button is pushed
    if 'voter' in request.GET and poll.open:
        try:
            response_dct['current_voter_id'] = int(request.GET['voter'])
        except ValueError:
            pass

    response_dct.update({'poll':poll,
                         'VOTE':Vote.VOTE,})
    response_dct['base_url'] = "/".join(request.path.split('/')[:-2]) \
                               + '/%s/' % poll.base_url

    # get voters and sum for each choice for this poll
    voters = Voter.objects.filter(poll=poll)
    choice_ids = [choice.id for choice in choices]
    for voter in voters:
        # highlight a voter
        if time.mktime(voter.modification_date.timetuple()) \
                                                         == highlight_vote_date:
            voter.highlight = True
        voter.votes = voter.getVotes(choice_ids)
        # initialize undefined vote
        choice_vote_ids = [vote.choice.id for vote in voter.votes]
        for choice in choices:
            if choice.id not in choice_vote_ids:
                vote = Vote(voter=voter, choice=choice, value=None)
                vote.save()
                idx = choices.index(choice)
                voter.votes.insert(idx, vote)
    sums = [choice.getSum(poll.type == 'B') for choice in choices]
    vote_max = max(sums)
    c_idx = 0
    while c_idx < len(choices):
        try:
            c_idx = sums.index(vote_max, c_idx)
            choices[c_idx].highlight = True
            c_idx += 1
        except ValueError:
            c_idx = len(choices)
    # set non-available choices if the limit is reached for a choice
    response_dct['limit_set'] = None
    for choice in choices:
        if choice.limit:
           response_dct['limit_set'] = True
        if choice.limit and sums[choices.index(choice)] >= choice.limit:
            choice.available = False
        else:
            choice.available = True
        choice.save()
    response_dct['voters'] = voters
    response_dct['choices'] = choices
    response_dct['comments'] = Comment.objects.filter(poll=poll)
    # verify if vote's result has to be displayed
    response_dct['hide_vote'] = True
    if u'display_result' in request.GET:
        request.session['knowned_vote_' + poll.base_url] = 1
    if 'knowned_vote_' + poll.base_url in request.session:
        response_dct['hide_vote'] = False
    return render_to_response('vote.html', response_dct)
