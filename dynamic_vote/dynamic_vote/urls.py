
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import login, logout
from django.views.generic.edit import CreateView

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url('^register/$',
        CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
        ),
        name='register'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('voting.urls')),
]
