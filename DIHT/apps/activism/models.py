from django.contrib.auth.models import User
from django.db.models import \
    PositiveSmallIntegerField, ForeignKey, DateTimeField, \
    DateField, BooleanField, OneToOneField,\
    Model, CharField, ManyToManyField, TextField


class Task(Model):
    name = CharField("Название")
    description = TextField("Описание")
    author = ForeignKey(User)
    hours = PositiveSmallIntegerField()
    executors = ManyToManyField(User)
    status = CharField()
    datetime_limit = DateTimeField()
    datetime_open = DateTimeField()
    datetime_done = DateTimeField()

