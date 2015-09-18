from django.conf.urls import url
from django.views.generic import TemplateView
from main.views import GymView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    url(r'^gym/$', GymView.as_view(template_name="gym.html"), name='gym'),
    url(r'^feedback/$', TemplateView.as_view(template_name="feedback.html"), name='feedback'),
    # url(r'^accommodation/$', TemplateView.as_view(template_name="accommodation.html"), name='accommodation'),
    # url(r'^announcements/$', TemplateView.as_view(template_name="announcements.html"), name='announcements'),
    url(r'^403/$', TemplateView.as_view(template_name="503.html"), name='403'),
]