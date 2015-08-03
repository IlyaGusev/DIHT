from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    url(r'^gym/$', TemplateView.as_view(template_name="gym.html"), name='gym'),
    url(r'^accommodation/$', TemplateView.as_view(template_name="accommodation.html"), name='accommodation'),
    url(r'^announcements/$', TemplateView.as_view(template_name="announcements.html"), name='announcements'),
	url(r'^test/$', TemplateView.as_view(template_name="active/event.html"), name='test'),
]