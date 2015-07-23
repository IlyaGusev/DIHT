from django.conf.urls import url
from accounts.views import SignUpView

urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
]