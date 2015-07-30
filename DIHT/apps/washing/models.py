from django.contrib.auth.models import User
from django.db.models import \
    PositiveSmallIntegerField, ForeignKey, DateTimeField, \
    DateField, BooleanField, OneToOneField,\
    Model, CharField, ManyToManyField


class Parameters(Model):
    date = DateField()
    delta_hour = PositiveSmallIntegerField()
    delta_minute = PositiveSmallIntegerField()
    start_hour = PositiveSmallIntegerField()
    start_minute = PositiveSmallIntegerField()
    price = PositiveSmallIntegerField()

    def __str__(self):
        return 'Price: '+str(self.price)+\
               '; Delta: '+str(self.delta_hour) + '-' + str(self.delta_minute) + \
               '; Start: '+str(self.start_hour) + '-' + str(self.start_minute)


class WashingMachine(Model):
    is_active = BooleanField(default=True)
    name = CharField(max_length=50)
    parameters = ManyToManyField(Parameters, related_name='machines')

    def __str__(self):
        return self.name


class WashingMachineRecord(Model):
    machine = ForeignKey(WashingMachine, related_name='records')
    user = ForeignKey(User)
    datetime_from = DateTimeField()
    datetime_to = DateTimeField()

    def __str__(self):
        return str(self.machine)+'; '+str(self.user.last_name) + '; ' + str(self.datetime_from)


class RegularNonWorkingDay(Model):
    day_of_week = PositiveSmallIntegerField()
    machine = ForeignKey(WashingMachine, related_name='regular_non_working_days')

    def __str__(self):
        return str(self.machine)+'; '+str(self.day_of_week)

class NonWorkingDay(Model):
    date = DateField()
    machine = ForeignKey(WashingMachine, related_name='non_working_days')

    def __str__(self):
        return str(self.machine)+'; '+str(self.date)


class BlackListRecord(Model):
    user = OneToOneField(User)
    always = BooleanField()
    date_to = DateField(null=True)

