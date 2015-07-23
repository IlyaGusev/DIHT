from django.conf.urls import url
from django.views.generic import TemplateView
from accounts.views import SignUpView, ResetPasswordView

urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signup_ok/$', TemplateView.as_view(template_name='accounts/signup_ok.html'), name='signup_ok'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^reset_password/$', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^reset_password_ok/$', TemplateView.as_view(template_name='accounts/reset_password_ok.html'), name='reset_password_ok'),
]