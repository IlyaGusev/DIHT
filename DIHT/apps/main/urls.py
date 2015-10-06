from django.conf.urls import url
from django.views.generic import TemplateView
from main.views import GymView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    url(r'^gym/$', GymView.as_view(template_name="gym.html"), name='gym'),
    url(r'^feedback/$', TemplateView.as_view(template_name="feedback.html"), name='feedback'),
]