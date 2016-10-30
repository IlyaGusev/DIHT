# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания: 22/07/2015
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Формы, связанные с профилями пользователей.
"""
import re
import autocomplete_light
from django.forms import ValidationError, ModelForm, Form, CharField, PasswordInput, TextInput, TypedChoiceField, IntegerField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from accounts.models import Profile, Key


class SignUpForm(ModelForm):
    """
    Регистрационная форма.
    """
    middle_name = CharField(label=_('Отчество'), widget=TextInput(attrs={'placeholder': _('Отчество')}))
    sex = TypedChoiceField(label=_("Пол"),
                           coerce=lambda x: x == 'Женский',
                           choices=((False, 'Мужской'), (True, 'Женский')))
    hostel = CharField(label=_('Общежитие'), widget=TextInput(attrs={'placeholder': _('Общежитие')}), required=False)
    room_number = CharField(label=_('Номер комнаты'), widget=TextInput(attrs={'placeholder': _('Номер комнаты')}), required=False)
    group_number = CharField(label=_('Номер группы'), widget=TextInput(attrs={'placeholder': _('Номер группы')}), required=False)
    mobile = CharField(label=_('Номер телефона'), widget=TextInput(attrs={'placeholder': _('+71234567890')}))
    password = CharField(label=_('Пароль'), widget=PasswordInput(attrs={'placeholder': _('Пароль')}))
    password_repeat = CharField(label=_('Пароль ещё раз'), widget=PasswordInput(attrs={'placeholder': _('Пароль ещё раз')}))

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name', )
        labels = {
            'username': _('Логин'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('E-mail'),
        }
        widgets = {
            'username': TextInput(attrs={'placeholder': _('Логин')}),
            'first_name': TextInput(attrs={'placeholder': _('Имя')}),
            'last_name': TextInput(attrs={'placeholder': _('Фамилия')}),
            'email': TextInput(attrs={'placeholder': _('E-mail')}),
        }

    def clean_password_repeat(self):
        pass1 = self.data['password']
        pass2 = self.data['password_repeat']
        if pass1 != pass2:
            raise ValidationError(
                _("Пароли не совпадают."))
        return pass2

    def clean_username(self):
        r = re.compile('^[a-zA-Z][a-zA-Z0-9_-]*$')
        res = r.match(self.cleaned_data['username'])
        if res is None or len(self.cleaned_data['username']) <= 4:
            raise ValidationError(
                _('Некорректный логин.'))
        if User.objects.all().filter(username=self.cleaned_data['username']).count() > 0:
            raise ValidationError(
                _('Логин уже используется.'))
        return self.cleaned_data['username']

    def clean_first_name(self):
        r = re.compile(u'^[А-ЯЁ][а-яё]*$', re.UNICODE)
        res = r.match(self.cleaned_data['first_name'])
        if res is None:
            raise ValidationError(
                _('Неверный формат имени: первыя буква должна быть заглавной, допустимы только русские символы.'))
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        r = re.compile(u'^[А-ЯЁ][а-яё]+$', re.UNICODE)
        res = r.match(self.cleaned_data['last_name'])
        if res is None:
            raise ValidationError(
                _('Неверный формат фамилии: первыя буква должна быть заглавной, допустимы только русские символы.'))
        return self.cleaned_data['last_name']

    def clean_mobile(self):
        r = re.compile('^\+7[0-9]{10,10}$')
        res = r.match(self.cleaned_data['mobile'])
        if res is None:
            raise ValidationError(_('Некорректный номер телефона.'))
        return self.cleaned_data['mobile']

    def clean_middle_name(self):
        r = re.compile(u'^[А-ЯЁ][ёа-я]+$', re.UNICODE)
        res = r.match(self.cleaned_data['middle_name'])
        if res is None:
            raise ValidationError(
                _('Неверный формат отчества: первыя буква должна быть заглавной, допустимы только русские символы.'))
        return self.cleaned_data['middle_name']

    def clean_password(self):
        l = len(self.cleaned_data['password'])
        if l <= 5 or l >= 30:
            raise ValidationError(
                _('Неверная длина пароля.'))
        return self.cleaned_data['password']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(_('Этот e-mail уже используется.'))
        return self.cleaned_data['email']


class ProfileForm(ModelForm):
    """
    Форма изменения профиля.
    """
    class Meta:
        model = Profile
        fields = ('group_number', 'hostel', 'room_number', 'mobile', )

        labels = {
            'room_number': _('Номер комнаты'),
            'group_number': _('Номер группы'),
            'hostel': _('Общежитие'),
            'mobile': _('Номер телефона'),
        }
        widgets = {
            'room_number': TextInput(attrs={'placeholder': _('Номер комнаты')}),
            'group_number': TextInput(attrs={'placeholder': _('Номер группы')}),
            'hostel': TextInput(attrs={'placeholder': _('Общежитие')}),
            'mobile': TextInput(attrs={'placeholder': _('+71234567890')}),
        }

    def clean_mobile(self):
        r = re.compile('^\+7[0-9]{10,10}$')
        res = r.match(self.cleaned_data['mobile'])
        if res is None:
            raise ValidationError(_('Некорректный номер телефона.'))
        return self.cleaned_data['mobile']

    def clean_middle_name(self):
        r = re.compile(u'^[А-Яёа-я]+$', re.UNICODE)
        res = r.match(self.cleaned_data['middle_name'])
        if res is None:
            raise ValidationError(
                _('Неверный формат отчества: первыя буква должна быть заглавной, допустимы только русские символы.'))
        return self.cleaned_data['middle_name']


class ResetPasswordForm(Form):
    """
    Форма сброса пароля.
    """
    username = CharField(max_length=255, required=True, label='Логин', widget=TextInput(attrs={'placeholder': _('Логин')}))

    def clean_username(self):
        r = re.compile('^[a-zA-Z][a-zA-Z0-9_-]*$')
        res = r.match(self.cleaned_data['username'])
        if res is None:
            raise ValidationError(u'Некорректный логин')
        if User.objects.all().filter(username=self.cleaned_data['username']).count() != 1:
            raise ValidationError(u'Некорректный логин')
        return self.cleaned_data['username']


class ChangePasswordForm(ModelForm):
    """
    Форма изменения пароля.
    """
    old_password = CharField(widget=PasswordInput(), label="Старый пароль")
    password = CharField(widget=PasswordInput(), label="Новый пароль")
    password_repeat = CharField(widget=PasswordInput(), label="Повторите новый пароль")

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password_repeat')

    def clean_old_password(self):
        data = self.cleaned_data['old_password']
        if not self.instance.check_password(data):
            raise ValidationError("Старый пароль неправильный")
        return data

    def clean_password(self):
        l = len(self.cleaned_data['password'])
        if l <= 5 or l >= 30:
            raise ValidationError(_('Слишком маленький или слишком большой пароль'))
        return make_password(self.cleaned_data['password'])

    def clean_password_repeat(self):
        pass1 = self.data['password']
        pass2 = self.data['password_repeat']
        if pass1 != pass2:
            raise ValidationError("Пароли не совпадают")
        return pass2


class FindForm(Form):
    """
    Форма поиска пользователя с автодополнением.
    """
    user = autocomplete_light.ModelChoiceField('ProfileAutocomplete', label="Пользователь")


class MoneyForm(ModelForm):
    """
    Форма для ввода количества денег. Пустое поле fields и ModelForm - хак для использования UpdateView.
    """
    amount = IntegerField(min_value=0, max_value=10000, label="Количество")

    class Meta:
        model = Profile
        fields = []


class KeyCreateForm(autocomplete_light.ModelForm):
    """
    Форма для создания ключа.
    """
    owner_autocomplete = autocomplete_light.ModelChoiceField('ProfileAutocomplete',required=True, label=_('Владелец'))

    class Meta:
        model = Key
        fields = ('name', )
        labels = {
            'name': _('Название'),
        }


class KeyUpdateForm(autocomplete_light.ModelForm):
    """
    Форма для перемещения ключа. Пустое поле fields и ModelForm - хак для использования UpdateView.
    """
    second_owner_autocomplete = autocomplete_light.ModelChoiceField('ProfileAutocomplete', required=True, label=_('Кому'))

    class Meta:
        model = Key
        fields = []


class ChangePassIdForm(ModelForm):
    """
    Форма изменения UID пропуска.
    """
    class Meta:
        model = Profile
        fields = ('pass_id',)

    def clean_pass_id(self):
        data = self.cleaned_data['pass_id']
        return data.lower() if len(data) > 0 else None
