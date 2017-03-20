from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Q


class Poll(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    private = models.BooleanField(default=False, blank=True)
    creator = models.ForeignKey(User, default=None, blank=True, null=True)

    def get_top_voted_options(self, number=3):
        return self.options.annotate(num_votes=Count('votes')).filter(num_votes__gt=0).order_by('-num_votes')[:number]

    def __str__(self):
        return '({}) {} by {}'.format(self.id, self.title, self.creator)

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

    def __str__(self):
        return '{}@"{}"'.format(self.user, self.poll)


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, related_name='options')
    text = models.CharField(max_length=128)
    creator = models.ForeignKey(User)

    def __str__(self):
        return '{} by {} for {}'.format(self.text, self.creator, self.poll)


class Vote(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(PollOption, related_name='votes')
    score = models.IntegerField(default=0)

    def __str__(self):
        return '{} votes {} ({})'.format(self.user, self.option, self.score)
