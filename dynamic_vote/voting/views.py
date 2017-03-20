from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import PollForm
from .models import Poll, PollMember, PollOption, Vote


class PollsView(View):

    def get(self, request, *args, **kwargs):
        return self.render_polls(request)

    def post(self, request, *args, **kwargs):
        return self.render_polls(request)

    def render_polls(self, request):
        user = request.user
        my_polls = None
        if user.is_authenticated():
            my_polls = Poll.get_polls_for(user)
        return render(request, 'polls.html', {
            'user': user,
            'my_polls': my_polls,
        })


class PollView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, id, *args, **kwargs):
        user = request.user
        poll = get_object_or_404(Poll, id=id)
        if poll.private:
            get_object_or_404(PollMember, poll=poll, user=user)
        return self.render_poll(request, poll)

    def post(self, request, id, *args, **kwargs):
        user = request.user
        poll = get_object_or_404(Poll, id=id)
        if poll.private:
            get_object_or_404(PollMember, poll=poll, user=user)
        option_id = request.POST.get('option', None)
        if option_id:
            option = PollOption.objects.get(id=option_id)
            vote = Vote.objects.filter(user=user, option__poll=poll).first()
            if vote:
                vote.option = option
            else:
                vote = Vote(user=user, option=option, score=1)
            vote.save()
        add_element = request.POST.get('add_element', '')
        if add_element:
            if PollOption.objects.filter(text=add_element, poll=poll).count() == 0:
                option = PollOption(text=add_element, poll=poll, creator=user)
                option.save()
        delete_id = request.POST.get('delete', '')
        if delete_id:
            option = get_object_or_404(PollOption, creator=user, id=delete_id)
            option.delete()
        return self.render_poll(request, poll)

    def render_poll(self, request, poll):
        user = request.user
        options = PollOption.objects.filter(poll=poll)
        options_struct = []
        max_score = 0
        min_score = 0
        for option in options:
            score = 0
            for vote in Vote.objects.filter(option=option):
                score += vote.score
            options_struct.append({'option': option, 'score': score})
            if score > max_score:
                max_score = score
            elif score < min_score:
                min_score = score
        my_vote = Vote.objects.filter(option__poll=poll, user=user).first()
        my_polls = Poll.get_polls_for(user)
        return render(request, 'poll.html', {
            'poll': poll,
            'options_struct': options_struct,
            'my_vote': my_vote,
            'max_score': max_score,
            'min_score': min_score,
            'user': user,
            'my_polls': my_polls,
        })


class CreatePollView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        poll_form = PollForm()
        my_polls = Poll.get_polls_for(user)
        return render(request, 'create_poll.html', {
            'user': user,
            'my_polls': my_polls,
            'poll_form': poll_form,
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.creator = user
            poll.save()
            return redirect('poll', id=poll.id)
        else:
            my_polls = Poll.get_polls_for(user)
            return render(request, 'create_poll.html', {
                'user': user,
                'my_polls': my_polls,
                'poll_form': poll_form,
            })