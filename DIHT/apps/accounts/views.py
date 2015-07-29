from django.views.generic.edit import FormView, UpdateView
from django.views.generic import DetailView, View
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.core.mail import EmailMessage
from accounts.forms import UserProfileForm, SignUpForm, ResetPasswordForm
from accounts.models import UserProfile
from django.http import JsonResponse

import logging
logger = logging.getLogger('DIHT.custom')


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:signup_ok')

    def form_valid(self, form):
        SignUpView.register_user(form.cleaned_data)
        return super(SignUpView, self).form_valid(form)

    @classmethod
    @transaction.atomic
    def register_user(cls, form):
        user = User.objects.create_user(username=form['username'],
                                        email=form['email'],
                                        password=form['password'],
                                        first_name=form['first_name'],
                                        last_name=form['last_name'])
        # profile = UserProfile.objects.create(user=user,
        #                                      room_number=pform['room_number'],
        #                                      group_number=pform['group_number'],
        #                                      money=0,
        #                                      is_activated=False,
        #                                      mobile=pform['mobile'],
        #                                      middle_name=pform['middle_name'],
        #                                      hostel=pform['hostel'],
        #                                      status=pform['status'],
        #                                      sex=pform['sex'])
        user.is_active = False
        user.save()
        logger.info('Пользователь '+str(form['first_name'])+' '+str(form['last_name'])+' ('+str(form['username'])+') только что зарегистрировался на сайте.')


class ResetPasswordView(FormView):
    template_name = 'accounts/reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('accounts:reset_password_ok')

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(form=ResetPasswordForm()))

    def form_valid(self, form):
        user = User.objects.all().filter(username=form.cleaned_data['username'])[0]
        password = User.objects.make_random_password()
        email = EmailMessage(u'Сброс пароля', u'Новый пароль для 2ka.fizteh.ru: ' + password, to=[user.email])
        if email.send() == 1:
            user.set_password(password)
            user.save()
            logger.info('Пользователь ' + user.get_full_name() + ' (' + user.username + ') изменил свой пароль через функцию восстановления пароля.')
        return super(ResetPasswordView, self).form_valid(form)


class ProfileView(DetailView):
    template_name = 'accounts/profile.html'
    model = User
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = self.get_object()
        context['profile'] = UserProfile.objects.get(user__id=user.id)
        return context


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "accounts/edit_profile.html"
    slug_field = 'id'
    slug_url_kwarg = 'id'
    success_url = reverse_lazy('main:home')

    def form_invalid(self, form):
        super(UserProfileUpdateView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


class CheckUsernameView(View):

    def get(self, request, *args, **kwargs):
        username = request.GET['username']
        if User.objects.all().filter(username=username).count() > 0:
            result = {'exist': "1"}
        else:
            result = {'exist': "0"}
        return JsonResponse(result, status=200)