from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import \
    PositiveSmallIntegerField, ForeignKey, DateTimeField, \
    DateField, BooleanField, OneToOneField, FloatField, \
    Model, CharField, ManyToManyField, TextField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.core.urlresolvers import reverse


class Event(Model):
    STATUS_CHOICES = (
        ('closed', 'Проведено'),
        ('open', 'Готовится'),
    )
    name = CharField("Название", max_length=50)
    creator = ForeignKey(User, verbose_name="Создатель")
    date_created = DateField("Дата создания", default=timezone.now)
    date_held = DateField("Дата проведения", default=timezone.now)
    description = TextField("Описание", blank=True)
    assignees = ManyToManyField(User, "Ответственные", related_name="events", blank=True)
    status = CharField("Статус", choices=STATUS_CHOICES, default='open', max_length=6)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def get_absolute_url(self):
        return reverse('activism:event', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.name)


class TaggedTask(TaggedItemBase):
    content_object = ForeignKey('Task')


class Task(Model):
    STATUS_CHOICES = (
        ('closed', 'Закрыто'),
        ('resolved', 'Готово'),
        ('in_progress', 'Выполняется'),
        ('open', 'Не назначено'),
        ('in_labor', 'На бирже'),
    )

    name = CharField("Название", max_length=50)
    creator = ForeignKey(User, verbose_name="Создатель", related_name="tasks_created")
    event = ForeignKey(Event, related_name="tasks", verbose_name="Мероприятие", blank=True, null=True)
    description = TextField("Описание", blank=True)
    tags = TaggableManager(through=TaggedTask)
    hours_predict = FloatField("Расчётное количество часов", blank=False, null=False)
    number_of_assignees = PositiveSmallIntegerField("Количество людей", blank=False, null=False)
    candidates = ManyToManyField(User, "Кандидаты", related_name="tasks_approve", blank=True)
    assignees = ManyToManyField(User, "Назначенные", through="AssigneeTask", blank=True)
    rejected = ManyToManyField(User, "Отклоненные", related_name="tasks_rejected", blank=True)
    datetime_created = DateTimeField("Время создания", default=timezone.now)
    datetime_limit = DateTimeField("До какого времени надо сделать", default=timezone.now)
    datetime_closed = DateTimeField("Время закрытия", blank=True, null=True)
    datetime_last_modified = DateTimeField("Время последнего изменения", default=timezone.now)
    status = CharField("Статус", choices=STATUS_CHOICES, default='open', max_length=15)
    is_urgent = BooleanField("Срочное", default=False)
    is_hard = BooleanField("Тяжёлое", default=False)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def get_absolute_url(self):
        return reverse('activism:task', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.datetime_last_modified = timezone.now()
        return super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)+" by "+str(self.creator)


class AssigneeTask(Model):
    user = ForeignKey(User, verbose_name="Назначенный", related_name='participates')
    task = ForeignKey(Task, verbose_name="Задача", related_name='participates')
    hours = FloatField("Реальные часы", blank=True, null=True)
    approved = BooleanField("Подтверждено", default=False)

    def __str__(self):
        return str(self.user)+" in "+str(self.task)