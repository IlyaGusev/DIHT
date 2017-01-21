# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания: 22/07/2015
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Модели, связанные с профилями пользователей.
"""
from django.db.models import Model, OneToOneField, BooleanField, CharField, \
    IntegerField, ForeignKey, DateTimeField, ImageField, PositiveIntegerField
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from django.core.validators import RegexValidator
import hashlib


class Profile(Model):
    """
    Модель профиля.
    """
    user = OneToOneField(User)
    sex = BooleanField("Пол", default=False)
    hostel = CharField("Общежитие", max_length=30, blank=True)
    room_number = CharField("Номер комнаты", max_length=30, blank=True)
    group_number = CharField("Номер группы", max_length=30, blank=True)
    money = IntegerField("Количество денег", blank=True, null=True, default=0)
    payments = IntegerField("Невыплачено поощрений", blank=True, null=True, default=0)
    mobile = CharField("Мобильный телефон", max_length=30, blank=True)
    middle_name = CharField("Отчество", max_length=30, blank=True)
    sign = CharField("Подпись", max_length=255, blank=True, null=True, default='')
    pass_id = CharField("ID пропуска", blank=True, null=True, default=None,
                        unique=True, max_length=20,
                        validators=[RegexValidator('([0-9a-f]{2}){4,10}'),])

    def __str__(self):
        return 'Профиль пользвателя: %s' % self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        permissions = (
            ("change_profile_pass_id", "Can change profile pass id"),
        )

    #TODO: Использовать CharField.empty_value после перехода на Django 1.11
    def save(self, *args, **kwargs):
        if self.pass_id == '':
            self.pass_id = None
        super(Profile, self).save(*args, **kwargs)


def upload_to(instance, filename):
    # Хэш для того, чтобы корректно обрабатывать аватарки с кириллическими именами
    return 'avatars/%s/%s' % (instance.user.username, hashlib.md5(filename.encode()).hexdigest()+filename[-4:])


class Avatar(Model):
    """
    Модель аватарок.
    """
    user = OneToOneField(User)
    img = ImageField(max_length=1024, blank=True, upload_to=upload_to)
    date_uploaded = DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Аватар пользвателя: %s' % self.user.username

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"

class GeneralMoneyOperation(Model):
    """
        Обобщённая модель денежных операций. Поддерживает отмену операции с возвращением денег.
    """
    user = ForeignKey(User, null=False, blank=False, related_name='%(class)s_operations', verbose_name="Юзер")
    amount = IntegerField("Количество", null=False, default=0)
    timestamp = DateTimeField("Дата", null=False, blank=False, default=timezone.now)
    description = CharField("Описание", max_length=150, null=True, blank=True)
    moderator = ForeignKey(User, related_name='%(class)s_moderated_operations',
                           null=True, blank=True, verbose_name="Модератор")
    is_approved = BooleanField("Подтверждено", default=False)

    field = ''

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(GeneralMoneyOperation, self).save(*args, **kwargs)
            old_amount = getattr(self.user.profile, self.field)
            setattr(self.user.profile, self.field, old_amount + self.amount)
            self.user.profile.save()
        else:
            super(GeneralMoneyOperation, self).save(*args, **kwargs)

    @transaction.atomic
    def cancel(self):
        setattr(self.user.profile, self.field, getattr(self.user.profile, self.field) - self.amount)
        self.user.profile.save()
        self.delete()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.timestamp) + ': ' + str(self.user.last_name) + '; ' + str(self.amount)


class MoneyOperation(GeneralMoneyOperation):
    """
        Модель денежных операций. Изначально планировалась неизменяемой, но для флага подтверждения
        пришлось убрать это свойство. Поддерживает отмену операции с возвращением денег.
    """
    field = 'money'

    class Meta:
        verbose_name = "Денежная операция"
        verbose_name_plural = "Денежные операции"


class PaymentsOperation(GeneralMoneyOperation):
    """
        Модель денежных операций для поощрений
    """
    field = 'payments'

    class Meta:
        verbose_name = "Денежная операция поощрений"
        verbose_name_plural = "Денежные операции поощрений"


class Key(Model):
    """
    Модель ключа. Требовалась ребятам, которые заведуют стиралкой.
    """
    name = CharField("Описание", max_length=150)
    owner = ForeignKey(User, null=False, blank=False, related_name='keys', verbose_name="Владелец")

    class Meta:
        verbose_name = "Ключ"
        verbose_name_plural = "Ключи"

    def __str__(self):
        return str(self.name) + ': ' + str(self.owner.last_name)


class KeyTransfer(Model):
    """
    Модель передачи ключа.
    """
    key = ForeignKey(Key, null=False, blank=False, related_name='transfers', verbose_name="Передачи")
    first_owner = ForeignKey(User, null=False, blank=False, related_name='keys_first', verbose_name="От кого")
    second_owner = ForeignKey(User, null=False, blank=False, related_name='keys_second', verbose_name="К кому")
    timestamp = DateTimeField("Дата", null=False, blank=False, default=timezone.now)

    class Meta:
        verbose_name = "Передача ключа"
        verbose_name_plural = "Передачи ключа"

    def __str__(self):
        return (str(self.key.name) + ' at ' + str(self.timestamp) + ' from' +
                str(self.first_owner.last_name) + ' to ' + str(self.second_owner.last_name))
