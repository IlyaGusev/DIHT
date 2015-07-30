from django.conf.urls import url
from django.views.generic import TemplateView
from accounts.views import SignUpView, ResetPasswordView, ProfileView, ProfileUpdateView, CheckUsernameView

urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signup_ok/$', TemplateView.as_view(template_name='accounts/signup_ok.html'), name='signup_ok'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^reset_password/$', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^reset_password_ok/$', TemplateView.as_view(template_name='accounts/reset_password_ok.html'), name='reset_password_ok'),

    url(r'^profile/(?P<id>[0-9]*)/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/edit/(?P<id>[0-9]*)/$', ProfileUpdateView.as_view(), name='edit_profile'),

    url(r'^check_username/$', CheckUsernameView.as_view(), name='check_username'),
]