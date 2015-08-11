from django.conf.urls import url
from activism.views import EventView, TaskView, IndexView, DoTaskView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^events/(?P<id>[0-9]*)/$', EventView.as_view(), name='event'),
    url(r'^tasks/(?P<id>[0-9]*)/do$', DoTaskView.as_view(), name='do_task'),
    url(r'^tasks/(?P<id>[0-9]*)/$', TaskView.as_view(), name='task'),
]