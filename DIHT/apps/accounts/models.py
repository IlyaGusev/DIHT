from django.db.models import Model, OneToOneField, BooleanField, CharField, IntegerField, ForeignKey, DateTimeField
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.translation import ugettext_lazy as _



class Profile(Model):
    user = OneToOneField(User)
    sex = BooleanField()
    hostel = CharField(max_length=30, blank=True)
    room_number = CharField(max_length=30, blank=True)
    group_number = CharField(max_length=30, blank=True)
    money = IntegerField(blank=True)
    mobile = CharField(max_length=30, blank=True)
    middle_name = CharField(max_length=30, blank=True)


    def __str__(self):
        return u'Profile of user: %s' % self.user.username


class Permission(Model):
    class Meta:
        permissions = (
            ('in_charge_of_finance', 'Ответственный за финансы'),
            ('in_charge_of_users', 'Ответственный за работу с пользователями'),
            ('in_charge_of_washing', 'Ответственный за стиралку'),
        )


class MoneyOperation(Model):
    user = ForeignKey(User, null=False, blank=False, related_name='operations')
    amount = IntegerField(null=False)
    timestamp = DateTimeField(null=False, blank=False)
    description = CharField(max_length=150, null=True, blank=True)
    moderator = ForeignKey(User, related_name='moderated_operations', null=True, blank=True)

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

    def __str__(self):
        return str(self.timestamp)+': '+str(self.user.last_name)+'; '+str(self.amount)
