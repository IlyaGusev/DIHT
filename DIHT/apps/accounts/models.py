from django.db.models import Model, OneToOneField, BooleanField, CharField, \
    IntegerField, ForeignKey, DateTimeField, ImageField
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
import hashlib


class Profile(Model):
    user = OneToOneField(User)
    sex = BooleanField("Пол", default=False)
    hostel = CharField("Общежитие", max_length=30, blank=True)
    room_number = CharField("Номер комнаты", max_length=30, blank=True)
    group_number = CharField("Номер группы", max_length=30, blank=True)
    money = IntegerField("Количество денег", blank=True, null=True, default=0)
    mobile = CharField("Мобильный телефон", max_length=30, blank=True)
    middle_name = CharField("Отчество", max_length=30, blank=True)
    sign = CharField("Подпись", max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return 'Профиль пользвателя: %s' % self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


def upload_to(instance, filename):
    return 'avatars/%s/%s' % (instance.user.username, hashlib.md5(filename.encode()).hexdigest()+filename[-4:])


class Avatar(Model):
    user = OneToOneField(User)
    img = ImageField(max_length=1024, blank=True, upload_to=upload_to)
    date_uploaded = DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Аватар пользвателя: %s' % self.user.username

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"


class MoneyOperation(Model):
    user = ForeignKey(User, null=False, blank=False, related_name='operations', verbose_name="Юзер")
    amount = IntegerField("Количество", null=False, default=0)
    timestamp = DateTimeField("Дата", null=False, blank=False, default=timezone.now)
    description = CharField("Описание", max_length=150, null=True, blank=True)
    moderator = ForeignKey(User, related_name='moderated_operations',
                           null=True, blank=True, verbose_name="Модератор")
    is_approved = BooleanField("Подтверждено", default=False)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(MoneyOperation, self).save(*args, **kwargs)
            self.user.profile.money += self.amount
            self.user.profile.save()
        else:
            super(MoneyOperation, self).save(*args, **kwargs)


    @transaction.atomic
    def cancel(self):
        self.user.profile.money -= self.amount
        self.user.profile.save()
        self.delete()

    class Meta:
        verbose_name = "Денежная операция"
        verbose_name_plural = "Денежные операции"

    def __str__(self):
        return str(self.timestamp) + ': ' + str(self.user.last_name) + '; ' + str(self.amount)
