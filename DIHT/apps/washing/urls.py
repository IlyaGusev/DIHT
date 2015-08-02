from django.conf.urls import url
from washing.views import IndexView, CreateRecordView, CancelRecordView, BlockDayView, UnblockDayView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create_record/$', CreateRecordView.as_view(), name='create_record'),
    url(r'^cancel_record/$', CancelRecordView.as_view(), name='cancel_record'),
    url(r'^block_day/$', BlockDayView.as_view(), name='block_day'),
    url(r'^unblock_day/$', UnblockDayView.as_view(), name='unblock_day'),
]