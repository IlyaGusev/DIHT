# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания: 22/07/2015
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        URL resolver модуля accounts.
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from accounts.views import SignUpView, ResetPasswordView, ProfileView, ProfileUpdateView, \
    CheckUniqueView, AvatarUpdateView, SignUpOkView, FindView, AddMoneyView, RemoveMoneyView, \
    ActivateView, MoneyHistoryView, UserMoneyHistoryView, AddPaymentsView, RemovePaymentsView, ChangePasswordView, \
    ApproveMoneyView, KeysView, KeyCreateView, KeyUpdateView, KeyDeleteView, ChargeView, ChangePassIdView, \
    YandexMoneyFormView, YandexMoneyCardRedirView, YandexMoneyRedirView

urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signup_ok/$', SignUpOkView.as_view(), name='signup_ok'),
    url(r'^charge/$', ChargeView.as_view(), name='charge'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^reset_password/$', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^reset_password_ok/$', TemplateView.as_view(template_name='accounts/reset_password_ok.html'), name='reset_password_ok'),

    url(r'^profile/(?P<pk>[0-9]*)/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/edit/(?P<pk>[0-9]*)/$', ProfileUpdateView.as_view(), name='edit_profile'),
    url(r'^profile/add_money/(?P<pk>[0-9]*)/$', AddMoneyView.as_view(), name='add_money'),
    url(r'^profile/remove_money/(?P<pk>[0-9]*)/$', RemoveMoneyView.as_view(), name='remove_money'),
    url(r'^profile/history_money/(?P<pk>[0-9]*)/$', UserMoneyHistoryView.as_view(), name='history_money'),
    url(r'^profile/add_payments/(?P<pk>[0-9]*)/$', AddPaymentsView.as_view(), name='add_payments'),
    url(r'^profile/remove_payments/(?P<pk>[0-9]*)/$', RemovePaymentsView.as_view(), name='remove_payments'),
    url(r'^profile/find/$', FindView.as_view(), name='find'),
    url(r'^profile/approve_money/(?P<pk>[0-9]*)/$', ApproveMoneyView.as_view(), name='approve_money'),

    url(r'^change_password/(?P<pk>[0-9]*)/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^change_pass_id/(?P<pk>[0-9]*)/$', ChangePassIdView.as_view(), name='change_pass_id'),
    url(r'^activate/(?P<pk>[0-9]*)/$', ActivateView.as_view(), name='activate'),
    url(r'^money_history/$', MoneyHistoryView.as_view(), name='all_money_history'),
    url(r'^keys/$', KeysView.as_view(), name='keys'),
    url(r'^keys/create/$', KeyCreateView.as_view(), name='key_create'),
    url(r'^keys/(?P<pk>[0-9]*)/delete/$', KeyDeleteView.as_view(), name='key_delete'),
    url(r'^keys/(?P<pk>[0-9]*)/update/$', KeyUpdateView.as_view(), name='key_update'),

    url(r'^check_unique/$', CheckUniqueView.as_view(), name='check_unique'),
    url(r'^avatar/change/(?P<pk>[0-9]*)/$', AvatarUpdateView.as_view(), name='change_avatar'),

    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^yandex_money_form$', YandexMoneyFormView.as_view(), name='yandex_money_form'),
    url(r'^yandex_money_card$', YandexMoneyCardRedirView.as_view(), name='yandex_money_card'),
    url(r'^yandex_money_redir$', YandexMoneyRedirView.as_view(), name='yandex_money_redir'),
]
