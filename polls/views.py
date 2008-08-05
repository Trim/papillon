#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>
# This program can be distributed under the terms of the GNU GPL.
# See the file COPYING.

from random import choice
import string
import time

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from papillon.polls.models import Poll, PollUser, Choice, Vote

def getBaseResponse(request):
    url = "/".join([request.META['HTTP_HOST'], 
                    request.path.split('/')[1], '']) 
    return {'root_url':url}

def index(request):
    response_dct = getBaseResponse(request)
    error = ''
    if 'bad_poll' in request.GET:
        response_dct['error'] = "The poll requested don't exist (anymore?)"
    return render_to_response('main.html', response_dct)

def createOrEdit(request, admin_url):

    def genRandomURL():
        chars = string.letters + string.digits
        url = ''    
        for i in range(6):
            url += choice(chars)
        url += str(int(time.time()))
        return url
    
    response_dct = getBaseResponse(request)
    response_dct['TYPES'] = Poll.TYPE
    error = None
    poll = None
    if 'new' in request.POST:
        mandatory_fields = (('author_name', "Author name"),
                            ('poll_name', "Poll name"),
                            ('poll_desc', "Poll description"),
                            ('poll_type', "Poll type"),
                            )
        for key, label in mandatory_fields:
            if key not in request.POST or not request.POST[key]:
                if not error:
                    error = "%s is a mandatory field" % label
            else:
                response_dct[key] = request.POST[key]
        if error:
            response_dct['new'] = True
            response_dct['error'] = error
            response_dct['admin_url'] = \
                         "/".join(request.path.split('/')[:-2]) + '/0/'
        else:
            author = PollUser(name=request.POST['author_name'])
            author.save()
            base_url = 'b' + genRandomURL()
            admin_url = 'a' + genRandomURL()
            poll = Poll(name=request.POST['poll_name'],
description=request.POST['poll_desc'], author=author, base_url=base_url,
admin_url=admin_url, status = 'D', type=request.POST['poll_type'])
            poll.save()
            url = "/".join(request.path.split('/')[:-2]) \
                  + '/%s/' % poll.admin_url
            return HttpResponseRedirect(url)
    elif admin_url == '0':
        response_dct['new'] = True
        response_dct['admin_url'] = \
                         "/".join(request.path.split('/')[:-2]) + '/0/'
    else:
        try:
            poll = Poll.objects.filter(admin_url=admin_url)[0]
        except IndexError:
            url = "/".join(request.path.split('/')[:-2]) + '/0/'
            return HttpResponseRedirect(url)
        response_dct['choices'] = Choice.objects.filter(poll=poll).order_by('order')
        response_dct['author_name'] = poll.author.name
        response_dct['poll_name'] = poll.name
        response_dct['poll_desc'] = poll.description
        idx = [type[0] for type in poll.TYPE].index(poll.type)
        response_dct['type_name'] = Poll.TYPE[idx][1]
        response_dct['poll_status'] = poll.status
        response_dct['admin_url'] = \
       "/".join(request.path.split('/')[:-2]) + '/%s/' % poll.admin_url
        base_path = request.META['HTTP_HOST'] + \
                    "/".join(request.path.split('/')[:-3])
        response_dct['full_admin_url'] = base_path + "/edit/" \
                                         + admin_url + "/"
        response_dct['base_url'] = poll.base_url
        response_dct['full_base_url'] = base_path + "/poll/" \
                                   + poll.base_url + "/"
        response_dct['choiceform'] = "<input type='text' name='new_choice'/>"
        if 'new_choice' in request.POST and request.POST['new_choice']:
            try:
                order = Choice.objects.order_by('-order')[0].order
                order += 1
            except IndexError:
                order = 0
            choice = Choice(poll=poll, name=request.POST['new_choice'],
                            order=order) 
            choice.save()
        for key in request.POST:
            if key.startswith('delete_') and request.POST[key]:
                choice = Choice.objects.get(id=int(key[len('delete_'):]))
                Vote.objects.filter(choice=choice).delete()
                choice.delete()
    return render_to_response('createOrEdit.html', response_dct)


def poll(request, poll_url):
    response_dct = getBaseResponse(request)
    error = None
    try:
        poll = Poll.objects.filter(base_url=poll_url)[0]
    except IndexError:
        url = "/".join(request.path.split('/')[:-3])
        url += "?bad_poll=1"
        return HttpResponseRedirect(url)
    response_dct['base_url'] = \
       "/".join(request.path.split('/')[:-2]) + '/%s/' % poll.base_url
        
    choices = Choice.objects.filter(poll=poll).order_by('order')
    response_dct['choices'] = choices
    if 'author_name' in request.POST:
        if 'voter' in request.POST:
            try:
                author = PollUser.objects.filter(id=int(request.POST['voter']))[0]
            except ValueError, IndexError:
                author = None
            if author:
                author.name = request.POST['author_name']
                author.save()
                selected_choices = []
                for key in request.POST:
                    if key.startswith('vote_') and request.POST[key]:
                        try:
                            id = int(key.split('_')[1])
                            vote = Vote.objects.filter(id=id)[0]
                            if vote.choice not in choices:
                                raise ValueError
                            vote.vote = 1
                            vote.save()
                        except (ValueError, IndexError):
                            url = "/".join(request.path.split('/')[:-3])
                            url += "?bad_poll=1"
                            return HttpResponseRedirect(url)
                        selected_choices.append(vote.choice)
                for choice in choices:
                    if choice not in selected_choices:
                        try:
                            v = Vote.objects.filter(voter=author, choice=choice)[0]
                            v.vote = 0
                        except IndexError:
                            v = Vote(voter=author, choice=choice, vote=0)
                        v.save()
                
        else:
            author = PollUser(name=request.POST['author_name'])
            author.save()
            selected_choices = []
            for key in request.POST:
                if key.startswith('choice_') and request.POST[key]:
                    try:
                        id = int(key.split('_')[1])
                        choice = Choice.objects.filter(id=id)[0]
                        if choice not in choices:
                            raise ValueError
                    except (ValueError, IndexError):
                        url = "/".join(request.path.split('/')[:-3])
                        url += "?bad_poll=1"
                        return HttpResponseRedirect(url)
                    v = Vote(voter=author, choice=choice, vote=1)
                    selected_choices.append(choice)
                    v.save()
                for choice in choices:
                    if choice not in selected_choices:
                        v = Vote(voter=author, choice=choice, vote=0)
                        v.save()
    votes = Vote.objects.extra(where=['choice_id IN (%s)' \
                   % ",".join([str(choice.id) for choice in choices])])
    voters = []
    choices_sum = [0 for choice in choices]
    choices_ids = [choice.id for choice in choices]
    for vote in votes:
        if vote.voter not in voters:
            vote.voter.votes = [None for choice in choices]
            voters.append(vote.voter)
            voter = vote.voter
        else:
            voter = voters[voters.index(vote.voter)]
        idx = choices_ids.index(vote.choice.id)
        voter.votes[idx] = vote
        choices_sum[idx] += vote.vote
    response_dct['voters'] = voters
    if 'voter' in request.GET:
        try:
            response_dct['current_voter_id'] = int(request.GET['voter'])
        except ValueError:
            pass
    response_dct['voter'] = voters
    response_dct['choices_sum'] = [str(sum) for sum in choices_sum]
    response_dct['poll_type_name'] = poll.getTypeLabel()
    response_dct['poll_name'] = poll.name
    response_dct['poll_desc'] = poll.description
    return render_to_response('vote.html', response_dct)
