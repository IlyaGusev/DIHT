from django.conf.urls import url
from washing.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]