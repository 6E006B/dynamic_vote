from django.contrib import admin

from .models import Poll, PollMember, PollOption, Vote

admin.site.register(Poll)
admin.site.register(PollMember)
admin.site.register(PollOption)
admin.site.register(Vote)
