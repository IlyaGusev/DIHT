from django.forms import ValidationError, ModelForm, Form, IntegerField
from django.forms import CharField, PasswordInput, TextInput, TypedChoiceField, RadioSelect
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.contrib.auth.models import User
import re
from accounts.models import UserProfile

class HorizRadioRenderer(RadioSelect.renderer):
    def render(self):
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class SignUpForm(ModelForm):
    """
    Регистрационная форма.
    """

    password = CharField(label=_('Пароль'), widget=PasswordInput(attrs={'placeholder': _('Пароль')}))
    password_repeat = CharField(label=_('Пароль ещё раз'), widget=PasswordInput(attrs={'placeholder': _('Пароль ещё раз')}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )
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
                _("Пароли не совпадают"))
        return pass2

    def clean_username(self):
        r = re.compile('^[a-zA-Z][a-zA-Z0-9_-]*$')
        res = r.match(self.cleaned_data['username'])
        if res is None:
            raise ValidationError(
                _('Некорректный логин'))
        return self.cleaned_data['username']

    def clean_first_name(self):
        r = re.compile(u'^[А-Яа-яё]*$', re.UNICODE)
        res = r.match(self.cleaned_data['first_name'])
        if res is None:
            raise ValidationError(
                _('Неверный формат имени: первыя буква должна быть заглавной, допустимы только русские символы.'))
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        r = re.compile(u'^[А-Яа-яё]+$', re.UNICODE)
        res = r.match(self.cleaned_data['last_name'])
        if res is None:
            raise ValidationError(
                _('Неверный формат имени: первыя буква должна быть заглавной, допустимы только русские символы.'))
        return self.cleaned_data['last_name']

    def clean_email(self):
        r = re.compile(u'^.+@.+\..+$', re.UNICODE)
        res = r.match(self.cleaned_data['email'])
        if res is None:
            raise ValidationError(
                _('Неверный формат email.'))
        return self.cleaned_data['email']



class UserProfileForm(ModelForm):
    sex = TypedChoiceField(label=_("Пол"),
                           coerce=lambda x: x == 'Женский',
                           choices=((False, 'Мужской'), (True, 'Женский')))

    class Meta:
        model = UserProfile
        fields = ('middle_name', 'sex',  'group_number', 'hostel', 'room_number', 'mobile', )

        labels = {
            'room_number': _('Номер комнаты'),
            'group_number': _('Номер группы'),
            'hostel': _('Общежитие'),
            'mobile': _('Номер телефона'),
            'middle_name': _('Отчество'),
            'status': _('Статус'),
            'sex': _('Пол'),
        }
        widgets = {
            'room_number': TextInput(attrs={'placeholder': _('Номер комнаты')}),
            'group_number': TextInput(attrs={'placeholder': _('Номер группы')}),
            'hostel': TextInput(attrs={'placeholder': _('Общежитие')}),
            'mobile': TextInput(attrs={'placeholder': _('+71234567890')}),
            'middle_name': TextInput(attrs={'placeholder': _('Отчество')}),
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
    username = CharField(min_length=5, max_length=30, required=True)

    def clean_username(self):
        r = re.compile('^[a-zA-Z][a-zA-Z0-9_-]*$')
        res = r.match(self.cleaned_data['username'])
        if res is None:
            raise ValidationError(u'Некорректный логин')
        if User.objects.all().filter(username=self.cleaned_data['username']).count() != 1:
            raise ValidationError(u'Некорректный логин')
        return self.cleaned_data['username']

