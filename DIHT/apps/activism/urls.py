from django.conf.urls import url
from activism.views import EventView, TaskView, IndexView, TaskCreateView, \
    EventsView, EventCreateView, TaskActionView, EventActionView, UnlockView, \
    SectorView, ClosedTasksView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^unlock/$', UnlockView.as_view(), name='unlock'),
    url(r'^events/$', EventsView.as_view(), name='events'),
    url(r'^events/create/$', EventCreateView.as_view(), name='create_event'),
    url(r'^events/(?P<pk>[0-9]*)/$', EventView.as_view(), name='event'),
    url(r'^events/(?P<pk>[0-9]*)/(?P<action>[0-9_a-z]+)$', EventActionView.as_view(), name='event_action'),
    url(r'^sector/(?P<pk>[0-9]*)/$', SectorView.as_view(), name='sector'),
    url(r'^tasks/(?P<pk>[0-9]*)/$', TaskView.as_view(), name='task'),
    url(r'^tasks/(?P<pk>[0-9]*)/(?P<action>[0-9_a-z]+)$', TaskActionView.as_view(), name='task_action'),
    url(r'^tasks/create/$', TaskCreateView.as_view(), name='create_task'),
    url(r'^tasks/closed/$', ClosedTasksView.as_view(), name='closed'),
]