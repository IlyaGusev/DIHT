from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
    STATUS_CHOICES = (
        ('Студент', _("Студент"),),
        ('Аспирант', _("Аспирант"),),
    )

    user = models.OneToOneField(User)
    room_number = models.CharField(max_length=30, blank=True)
    group_number = models.CharField(max_length=30, blank=True)
    money = models.SmallIntegerField(blank=True)
    sex = models.BooleanField(blank=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=False)
    hostel = models.CharField(max_length=30, blank=False, null=False)
    status = models.CharField(max_length=30, blank=False, null=False, choices=STATUS_CHOICES, default='Студент')

    def __str__(self):
        return u'Profile of user: %s' % self.user.username

class Permission(models.Model):
    class Meta:
        permissions = (
            ('in_charge_of_finance', 'Ответственный за финансы'),
            ('in_charge_of_users', 'Ответственный за работу с пользователями'),
            ('in_charge_of_washing', 'Ответственный за стиралку'),
        )