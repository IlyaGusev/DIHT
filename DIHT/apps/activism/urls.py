from django.conf.urls import url
from activism.views import EventView, TaskView, IndexView, DoTaskView, TaskCreateView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^events/(?P<pk>[0-9]*)/$', EventView.as_view(), name='event'),
    url(r'^tasks/(?P<pk>[0-9]*)/do$', DoTaskView.as_view(), name='do_task'),
    url(r'^tasks/(?P<pk>[0-9]*)/$', TaskView.as_view(), name='task'),
    url(r'^tasks/create/$', TaskCreateView.as_view(), name='create_task'),
]