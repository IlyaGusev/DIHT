from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    STATUS_CHOICES = (
        ('Студент', _("Студент"),),
        ('Аспирант', _("Аспирант"),),
    )

    user = models.OneToOneField(User)
    sex = models.BooleanField()
    hostel = models.CharField(max_length=30, blank=True)
    room_number = models.CharField(max_length=30, blank=True)
    group_number = models.CharField(max_length=30, blank=True)
    money = models.SmallIntegerField(blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)


    def __str__(self):
        return u'Profile of user: %s' % self.user.username

class Permission(models.Model):
    class Meta:
        permissions = (
            ('in_charge_of_finance', 'Ответственный за финансы'),
            ('in_charge_of_users', 'Ответственный за работу с пользователями'),
            ('in_charge_of_washing', 'Ответственный за стиралку'),
        )