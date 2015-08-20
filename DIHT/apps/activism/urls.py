from django.conf.urls import url
from activism.views import EventView, TaskView, IndexView, TaskCreateView, EventsView, EventCreateView, ChangeTaskStatusView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^events/$', EventsView.as_view(), name='events'),
    url(r'^events/create/$', EventCreateView.as_view(), name='create_event'),
    url(r'^events/(?P<pk>[0-9]*)/$', EventView.as_view(), name='event'),
    url(r'^tasks/(?P<pk>[0-9]*)/$', TaskView.as_view(), name='task'),
    url(r'^tasks/(?P<pk>[0-9]*)/(?P<action>[0-9_a-z]+)$', ChangeTaskStatusView.as_view(), name='task_action'),
    url(r'^tasks/create/$', TaskCreateView.as_view(), name='create_task'),
]