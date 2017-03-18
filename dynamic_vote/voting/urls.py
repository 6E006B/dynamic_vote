from django.conf.urls import url

from .views import CreatePollView, PollsView, PollView

urlpatterns = [
    url(r'^$', PollsView.as_view(), name='polls'),
    url(r'^poll/(?P<id>[a-zA-Z0-9]*)/$', PollView.as_view(), name='poll'),
    url(r'^create/', CreatePollView.as_view(), name='create-poll')
]