import os
from DIHT.settings import BASE_DIR
from django.core.files import File
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import DetailView, View, TemplateView, ListView
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, UserPassesTestMixin, GroupRequiredMixin
from django.utils import timezone
from itertools import chain
from accounts.forms import ProfileForm, SignUpForm, ResetPasswordForm, FindForm, \
    MoneyForm, ChangePasswordForm, KeyCreateForm, KeyUpdateForm
from accounts.models import Profile, Avatar, MoneyOperation, Key, KeyTransfer
from washing.models import BlackListRecord
from activism.views import get_level

import logging
logger = logging.getLogger('DIHT.custom')


class JsonErrorsMixin(object):
    def form_invalid(self, form):
        super(JsonErrorsMixin, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


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
        avatar = Avatar.objects.create(user=user)
        with open(os.path.join(BASE_DIR, 'DIHT/static/img/standart_avatar.png'), 'rb') as img_file:
            avatar.img.save("avatar", File(img_file), save=True)
        avatar.save()
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
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = self.get_object().user
        is_charge = Group.objects.get(name="Ответственные за активистов") in self.request.user.groups.all()
        is_activist = Group.objects.get(name="Активисты") in self.request.user.groups.all()
        context['records'] = user.records.order_by('-datetime_to').reverse()
        context['task_current'] = user.task_set.exclude(status__in=['closed', 'resolved'])
        context['task_responsible'] = sorted(user.tasks_responsible.all(),
                                             key=lambda task: task.datetime_created, reverse=True)
        context['task_hours'] = user.participated.filter(task__status__in=['closed', 'resolved'])
        if user.social_auth.filter(provider='vk-oauth2').exists():
            context['vk'] = user.social_auth.get(provider='vk-oauth2').uid
        if context['profile'].group_number != '':
            grade = int(str(timezone.now().date().year)[-1]) - int(str(context['profile'].group_number)[0])
            if timezone.now().date().month >= 8:
                grade += 1
            if grade > 6 or grade < 0:
                context['grade'] = 'Выпускник/Аспирант'
            else:
                context['grade'] = str(grade) + ' курс'
        context['can_view_tasks'] = (self.request.user == user and is_activist) or self.request.user.is_superuser or is_charge
        context['moderated_money'] = sum(user.moderated_operations.filter(is_approved=False, amount__gte=0)
                                                                  .values_list('amount', flat=True))
        context['operations'] = user.point_operations.all()
        context['op_for_hours'] = int(sum(user.participated.filter(task__status__in=['closed'])
                                              .values_list('hours', flat=True)) // 10)
        context['level'] = get_level(user)
        return context


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, JsonErrorsMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy('main:home')
    raise_exception = True

    def test_func(self, user):
        return self.get_object().user == user

    def form_valid(self, form):
        super(ProfileUpdateView, self).form_valid(form)
        return JsonResponse({'url': reverse('accounts:profile', kwargs={'pk': self.get_object().pk})}, status=200)


class AvatarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Avatar
    fields = ('img', )
    success_url = reverse_lazy('main:home')

    def test_func(self, user):
        return self.get_object().user == user


class SignUpOkView(TemplateView):
    template_name = 'accounts/signup_ok.html'

    def get_context_data(self, **kwargs):
        context = super(SignUpOkView, self).get_context_data(**kwargs)
        if Group.objects.filter(name='Ответственные за работу с пользователями').exists():
            context['charge'] = Group.objects.get(name='Ответственные за работу с пользователями').user_set.all()
        return context


class ChargeView(TemplateView):
    template_name = 'accounts/charge.html'

    def get_context_data(self, **kwargs):
        context = super(ChargeView, self).get_context_data(**kwargs)
        if Group.objects.filter(name='Ответственные за работу с пользователями').exists():
            context['charge'] = Group.objects.get(name='Ответственные за работу с пользователями').user_set.all()
        return context


class FindView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    template_name = 'accounts/find.html'
    form_class = FindForm
    group_required = ['Ответственные за работу с пользователями', 'Ответственные за финансы']
    raise_exception = True

    def form_valid(self, form):
        return JsonResponse({'url': reverse('accounts:profile',
                                            kwargs={'pk': form.cleaned_data['user'].profile.pk})},
                            status=200)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


class MoneyView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Profile
    form_class = MoneyForm
    group_required = 'Ответственные за финансы'
    raise_exception = True

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


class AddMoneyView(MoneyView):
    template_name = 'accounts/add_money.html'

    def form_valid(self, form):
        MoneyOperation.objects.create(user=self.get_object().user,
                                      amount=form.cleaned_data['amount'],
                                      timestamp=timezone.now(),
                                      description="Пополнение",
                                      moderator=self.request.user)
        return JsonResponse({'url': reverse('accounts:profile',
                                            kwargs={'pk': self.get_object().pk})},
                            status=200)


class RemoveMoneyView(MoneyView):
    template_name = 'accounts/remove_money.html'

    def form_valid(self, form):
        if self.get_object().money >= form.cleaned_data['amount']:
            MoneyOperation.objects.create(user=self.get_object().user,
                                          amount=-form.cleaned_data['amount'],
                                          timestamp=timezone.now(),
                                          description="Снятие",
                                          moderator=self.request.user)
        else:
            form.add_error('amount', "Недостаточно денег на счету")
            return super(RemoveMoneyView, self).form_invalid(form)
        return JsonResponse({'url': reverse('accounts:profile',
                                            kwargs={'pk': self.get_object().pk})},
                            status=200)


class ActivateView(SingleObjectMixin, LoginRequiredMixin, GroupRequiredMixin, View):
    model = User
    group_required = 'Ответственные за работу с пользователями'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return HttpResponseRedirect(reverse('accounts:profile', kwargs={'pk': self.get_object().profile.pk}))


class MoneyHistoryView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = MoneyOperation
    group_required = 'Ответственные за финансы'
    context_object_name = 'operations'
    template_name = "accounts/money_history.html"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(MoneyHistoryView, self).get_context_data(**kwargs)
        context['operations'] = MoneyOperation.objects.all().order_by('timestamp').reverse()
        return context


class UserMoneyHistoryView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = "accounts/money_history.html"
    raise_exception = True

    def test_func(self, user):
        return (user == self.get_object().user) or user.is_superuser or \
               (Group.objects.get(name='Ответственные за финансы') in user.groups.all())

    def get_context_data(self, **kwargs):
        context = super(UserMoneyHistoryView, self).get_context_data(**kwargs)
        context['operations'] = \
            sorted(chain(self.get_object().user.operations.exclude(moderator=self.get_object().user.pk),
                         self.get_object().user.moderated_operations.all()),
                   key=lambda instance: instance.timestamp, reverse=True)
        return context


class ChangePasswordView(LoginRequiredMixin, UserPassesTestMixin, JsonErrorsMixin, UpdateView):
    model = User
    form_class = ChangePasswordForm
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("main:home")
    raise_exception = True

    def test_func(self, user):
        return (user == self.get_object()) or user.is_superuser

    def form_valid(self, form):
        super(ChangePasswordView, self).form_valid(form)
        return JsonResponse({'url': reverse('accounts:profile', kwargs={'pk': self.get_object().profile.pk})},
                            status=200)


class ApproveMoneyView(LoginRequiredMixin, GroupRequiredMixin,  SingleObjectMixin, View):
    model = User
    group_required = 'Руководители финансов'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        for op in user.moderated_operations.filter(amount__gte=0, is_approved=False):
            op.is_approved = True
            op.save()
        return HttpResponseRedirect(reverse('accounts:profile', kwargs={'pk': user.profile.pk}))


class KeyCreateView(LoginRequiredMixin, GroupRequiredMixin, JsonErrorsMixin, FormView):
    model = Key
    template_name = 'accounts/add_key.html'
    form_class = KeyCreateForm
    group_required = 'Ответственные за стиралку'
    raise_exception = True
    success_url = reverse_lazy('accounts:keys')

    def form_valid(self, form):
        super(KeyCreateView, self).form_valid(form)
        Key.objects.create(name=form.cleaned_data['name'],
                           owner=form.cleaned_data['owner_autocomplete'])
        return JsonResponse({'url': reverse('accounts:keys')}, status=200)


class KeyUpdateView(LoginRequiredMixin, GroupRequiredMixin, JsonErrorsMixin, UpdateView):
    model = Key
    template_name = 'accounts/update_key.html'
    form_class = KeyUpdateForm
    group_required = 'Ответственные за стиралку'
    raise_exception = True

    def form_valid(self, form):
        KeyTransfer.objects.create(key=self.get_object(),
                                   first_owner=self.get_object().owner,
                                   second_owner=form.cleaned_data['second_owner_autocomplete'])
        key = Key.objects.get(pk=self.get_object().pk)
        key.owner = form.cleaned_data['second_owner_autocomplete']
        key.save()
        return JsonResponse({'url': reverse('accounts:keys')}, status=200)


class KeysView(LoginRequiredMixin, GroupRequiredMixin,  ListView):
    model = Key
    context_object_name = 'keys'
    template_name = 'accounts/keys.html'
    group_required = 'Ответственные за стиралку'
    raise_exception = True


class KeyDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Key
    group_required = 'Ответственные за стиралку'
    success_url = reverse_lazy('accounts:keys')
    raise_exception = True