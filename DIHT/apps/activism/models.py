from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import \
    PositiveSmallIntegerField, ForeignKey, DateTimeField, \
    DateField, BooleanField, OneToOneField, FloatField, \
    Model, CharField, ManyToManyField, TextField, ImageField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.core.urlresolvers import reverse


def upload_to_sector(instance, filename):
    return 'sectors/%s/%s' % (instance.name, filename)

    
class Sector(Model):
    name = CharField("Название", max_length=50)
    description = TextField("Описание", blank=True)
    main = ForeignKey(User, verbose_name="Руководитель", blank=True, null=True)
    photo = ImageField (max_length=1024, blank=True, upload_to=upload_to_sector)

    class Meta:
        verbose_name = "Сектор"
        verbose_name_plural = "Секторы"

    def __str__(self):
        return str(self.name)


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
    sector = ForeignKey(Sector, related_name="events", verbose_name="Сектор", blank=True, null=True)

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
    tags = TaggableManager(through=TaggedTask, blank=True)
    hours_predict = FloatField("Расчётное количество часов",
                               validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
                               blank=False, null=False)
    number_of_assignees = PositiveSmallIntegerField("Количество людей", blank=False, null=False)
    candidates = ManyToManyField(User, "Кандидаты", related_name="tasks_approve", blank=True)
    assignees = ManyToManyField(User, "Назначенные", through="AssigneeTask", blank=True)
    rejected = ManyToManyField(User, "Отклоненные", related_name="tasks_rejected", blank=True)
    datetime_created = DateTimeField("Время создания", default=timezone.now)
    datetime_limit = DateTimeField("До какого времени надо сделать", default=timezone.now)
    datetime_closed = DateTimeField("Время закрытия", blank=True, null=True)
    datetime_last_modified = DateTimeField("Время последнего изменения", default=timezone.now)
    status = CharField("Статус", choices=STATUS_CHOICES, default='open', max_length=15)
    sector = ForeignKey(Sector, related_name="tasks", verbose_name="Сектор", blank=True, null=True)
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
    user = ForeignKey(User, verbose_name="Назначенный", related_name='participated')
    task = ForeignKey(Task, verbose_name="Задача", related_name='participants')
    hours = FloatField("Реальные часы", blank=True, null=True,
                       validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    approved = BooleanField("Подтверждено", default=False)

    def __str__(self):
        return str(self.user)+" in "+str(self.task)


class PointOperation(Model):
    user = ForeignKey(User, null=False, blank=False, related_name='point_operations', verbose_name="Юзер")
    amount = FloatField("Количество", null=False, default=0)
    timestamp = DateTimeField("Дата", null=False, blank=False, default=timezone.now)
    description = CharField("Описание", max_length=150, null=True, blank=True)
    moderator = ForeignKey(User, related_name='moderated_point_operations',
                           null=True, blank=True, verbose_name="Ответственный")

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(PointOperation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Операция очков роста"
        verbose_name_plural = "Операции очков роста"

    def __str__(self):
        return str(self.timestamp)+': '+str(self.user.last_name)+'; '+str(self.amount)