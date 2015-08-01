from django.db.models import Model, OneToOneField, BooleanField, CharField, IntegerField, ForeignKey, DateTimeField
from django.contrib.auth.models import User
from django.db import transaction


class Profile(Model):
    user = OneToOneField(User)
    sex = BooleanField("Пол")
    hostel = CharField("Общежитие", max_length=30, blank=True)
    room_number = CharField("Номер комнаты", max_length=30, blank=True)
    group_number = CharField("Номер группы", max_length=30, blank=True)
    money = IntegerField("Количество денег", blank=True)
    mobile = CharField("Мобильный телефон", max_length=30, blank=True)
    middle_name = CharField("Отчество", max_length=30, blank=True)


    def __str__(self):
        return u'Profile of user: %s' % self.user.username


class MoneyOperation(Model):
    user = ForeignKey(User, null=False, blank=False, related_name='operations', verbose_name="Юзер")
    amount = IntegerField("Количество", null=False)
    timestamp = DateTimeField("Дата", null=False, blank=False)
    description = CharField("Описание", max_length=150, null=True, blank=True)
    moderator = ForeignKey(User, related_name='moderated_operations', null=True, blank=True,
                           verbose_name="Модератор")

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(MoneyOperation, self).save(*args, **kwargs)
            self.user.profile.money += self.amount
            self.user.profile.save()

    @transaction.atomic
    def cancel(self):
        self.user.profile.money -= self.amount
        self.user.profile.save()
        self.delete()

    class Meta:
        verbose_name = "Денежная операция"
        verbose_name_plural = "Денежные операции"

    def __str__(self):
        return str(self.timestamp)+': '+str(self.user.last_name)+'; '+str(self.amount)
