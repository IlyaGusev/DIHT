from django.conf.urls import url
from django.views.generic import TemplateView
from activism.views import EventView, TaskView, IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^event(?P<id>[0-9]*)/$', EventView.as_view(), name='event'),
    url(r'^task(?P<id>[0-9]*)/$', TaskView.as_view(), name='task'),
]