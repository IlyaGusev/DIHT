from django.views.generic.edit import FormView, UpdateView
from django.views.generic import DetailView, View
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.core.mail import EmailMessage
from accounts.forms import ProfileForm, SignUpForm, ResetPasswordForm
from accounts.models import Profile, Avatar
from washing.models import BlackListRecord
from django.http import JsonResponse
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

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
        Profile.objects.create(user=user,
                               room_number=form['room_number'],
                               group_number=form['group_number'],
                               money=0,
                               mobile=form['mobile'],
                               middle_name=form['middle_name'],
                               hostel=form['hostel'],
                               sex=form['sex'])

        BlackListRecord.objects.create(user=user, is_blocked=False)
        Avatar.objects.create(user=user)
        user.is_active = False
        user.save()
        # logger.info('Пользователь '+str(form['first_name'])+' '+str(form['last_name'])+' ('+str(form['username'])+') только что зарегистрировался на сайте.')


class ResetPasswordView(FormView):
    template_name = 'accounts/reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('accounts:reset_password_ok')

    def form_valid(self, form):
        user = User.objects.all().filter(username=form.cleaned_data['username'])[0]
        password = User.objects.make_random_password()
        email = EmailMessage(u'Сброс пароля', u'Новый пароль для 2ka.fizteh.ru: ' + password, to=[user.email])
        if email.send() == 1:
            user.set_password(password)
            user.save()
            # logger.info('Пользователь ' + user.get_full_name() + ' (' + user.username + ') изменил свой пароль через функцию восстановления пароля.')
        return super(ResetPasswordView, self).form_valid(form)


class CheckUniqueView(View):
    def get(self, request, *args, **kwargs):
        username = request.GET['username']
        email = request.GET['email']
        result = {'username': '0', 'email': '0'}
        if username != '':
            if User.objects.all().filter(username=username).exists():
                result['username'] = '1'
        if email != '':
            if User.objects.all().filter(email=email).exists():
                result['email'] = '1'
        return JsonResponse(result, status=200)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    model = User
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = self.get_object()
        context['records'] = user.records.filter(datetime_to__gte=timezone.now()).order_by('-datetime_to').reverse()
        context['profile'] = Profile.objects.get(user__id=user.id)
        context['task_hours'] = user.participated.filter(task__status__in=['closed', 'resolved'])
        if context['profile'].group_number != '':
            grade = int(str(timezone.now().date().year)[-1])-int(str(context['profile'].group_number)[0])
            if timezone.now().date().month >= 8:
                context['grade'] = grade+1
            else:
                context['grade'] = grade
        return context


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy('main:home')
    raise_exception = True

    def test_func(self, user):
        return self.get_object().user.id == user.id

    def form_invalid(self, form):
        super(ProfileUpdateView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


class AvatarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Avatar
    fields = ('img', )
    success_url = reverse_lazy('main:home')

    def test_func(self, user):
        return self.get_object().user.id == user.id
