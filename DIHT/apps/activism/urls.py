from django.conf.urls import url
from activism.views import EventView, TaskView, IndexView, TaskCreateView, \
    EventsView, EventCreateView, TaskActionView, EventCloseView, UnlockView, \
    SectorView, ActivistsView, TaskLogView, AddPointsView, DeletePointsView, \
    PaymentsView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^unlock/$', UnlockView.as_view(), name='unlock'),

    url(r'^events/$', EventsView.as_view(), name='events'),
    url(r'^events/create/$', EventCreateView.as_view(), name='create_event'),
    url(r'^events/(?P<pk>[0-9]*)/$', EventView.as_view(), name='event'),
    url(r'^events/(?P<pk>[0-9]*)/close/$', EventCloseView.as_view(), name='event_close'),

    url(r'^sectors/(?P<pk>[0-9]*)/$', SectorView.as_view(), name='sector'),

    url(r'^tasks/(?P<pk>[0-9]*)/$', TaskView.as_view(), name='task'),
    url(r'^tasks/(?P<pk>[0-9]*)/log/$', TaskLogView.as_view(), name='task_log'),
    url(r'^tasks/(?P<pk>[0-9]*)/(?P<action>[0-9_a-z]+)/$', TaskActionView.as_view(), name='task_action'),
    url(r'^tasks/create/$', TaskCreateView.as_view(), name='create_task'),

    url(r'^activists/$', ActivistsView.as_view(), name='activists'),
    url(r'^activists/(?P<pk>[0-9]*)/add_points/$', AddPointsView.as_view(), name='add_points'),
    url(r'^activists/(?P<pk>[0-9]*)/delete_points/$', DeletePointsView.as_view(), name='delete_points'),

    url(r'^payments/$', PaymentsView.as_view(), name='payments'),
]