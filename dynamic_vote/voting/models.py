from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Poll(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    private = models.BooleanField(default=False, blank=True)
    creator = models.ForeignKey(User, default=None, blank=True, null=True)

    @staticmethod
    def get_polls_for(user):
        user_polls = Poll.objects.filter(
            Q(creator=user) |
            Q(options__in=PollOption.objects.filter(creator=user)) |
            Q(options__in=PollOption.objects.filter(votes__in=Vote.objects.filter(user=user)))
        ).distinct()
        return user_polls


class PollMember(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll, related_name='members')


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, related_name='options')
    text = models.CharField(max_length=128)
    creator = models.ForeignKey(User)


class Vote(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(PollOption, related_name='votes')
    score = models.IntegerField(default=0)
