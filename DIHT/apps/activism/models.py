from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import \
    PositiveSmallIntegerField, ForeignKey, DateTimeField, \
    DateField, BooleanField, OneToOneField,\
    Model, CharField, ManyToManyField, TextField


class Event(Model):
    STATUS_CHOICES = (
        ('closed', 'Проведено'),
        ('open', 'Готовится'),
    )
    name = CharField("Название", max_length=50)
    creator = ForeignKey(User, verbose_name="Создатель")
    date_created = DateField("Дата создания", default=timezone.now)
    date_held = DateField("Дата проведения")
    description = TextField("Описание", blank=True)
    assignees = ManyToManyField(User, "Ответственные", related_name="events", blank=True)
    status = CharField("Статус", choices=STATUS_CHOICES, default='open', max_length=4)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return str(self.name)+" by "+str(self.creator)


class Task(Model):
    STATUS_CHOICES = (
        ('closed', 'Закрыто'),
        ('resolved', 'Готово'),
        ('in_progress', 'Выполняется'),
        ('open', 'Не назначено'),
        ('in_labor', 'На бирже'),
        ('volunteers', 'Есть кандидаты'),
    )

    name = CharField("Название", max_length=50)
    creator = ForeignKey(User, verbose_name="Создатель", related_name="tasks_created")
    datetime_created = DateTimeField("Время создания", default=timezone.now)
    event = ForeignKey(Event, related_name="tasks", verbose_name="Мероприятие", blank=True, null=True)
    description = TextField("Описание", blank=True)
    hours_predict = PositiveSmallIntegerField("Расчётное количество часов", blank=True, null=True)
    hours_real = PositiveSmallIntegerField("Реальное количество часов", blank=True, null=True)
    assignees = ManyToManyField(User, "Ответственные", related_name="tasks", blank=True)
    datetime_limit = DateTimeField("До какого времени надо сделать", blank=True)
    datetime_closed = DateTimeField("Время закрытия", blank=True)
    datetime_last_modified = DateTimeField("Время последнего изменения", blank=True)
    status = CharField("Статус", choices=STATUS_CHOICES, default='open', max_length=15)
    is_urgent = BooleanField(default=False)
    is_hard = BooleanField(default=False)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def save(self, *args, **kwargs):
        self.datetime_last_modified = timezone.now()
        return super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)+" by "+str(self.creator)


