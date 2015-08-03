from django.conf.urls import url
from django.views.generic import TemplateView
from activism.views import EventView, IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^event/(?P<id>[0-9]*)/$', EventView.as_view(), name='event'),
]