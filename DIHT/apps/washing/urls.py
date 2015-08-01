from django.conf.urls import url
from washing.views import IndexView, CreateRecordView, CancelRecordView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create_record/$', CreateRecordView.as_view(), name='create_record'),
    url(r'^cancel_record/$', CancelRecordView.as_view(), name='cancel_record')
]