# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания:
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Модели, связанные модулем активистов.
"""
import hashlib
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import \
    PositiveSmallIntegerField, ForeignKey, DateTimeField, \
    DateField, BooleanField, FloatField, Model, CharField, \
    ManyToManyField, TextField, ImageField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.core.urlresolvers import reverse


def upload_to_sector(instance, filename):
    # Хэш для того, чтобы корректно обрабатывать картинки с кириллическими именами
    return 'sectors/%s' % hashlib.md5(filename.encode()).hexdigest()+filename[-4:]


class Sector(Model):
    """
    Модель сектора.
    """
    name = CharField("Название", max_length=50)
    description = TextField("Описание", blank=True)
    main = ForeignKey(User, verbose_name="Руководитель", blank=True, null=True)
    photo = ImageField(max_length=1024, blank=True, upload_to=upload_to_sector)
    color = CharField(verbose_name="Цвет", max_length=6, default="aaaaaa",
                      validators=[RegexValidator("[^0-9a-fA-F]", inverse_match=True)])

    class Meta:
        verbose_name = "Сектор"
        verbose_name_plural = "Секторы"

    def __str__(self):
        return str(self.name)


class Event(Model):
    """
    Модель мероприятия.
    """
    STATUS_CHOICES = (
        ('closed', 'Проведено'),
        ('open', 'Готовится'),
    )
    name = CharField("Название", max_length=50)
    date_created = DateField("Дата создания", default=timezone.now)
    date_held = DateField("Дата проведения", default=timezone.now)
    description = TextField("Описание", blank=True)
    responsible = ManyToManyField(User, verbose_name="Ответственные", through="ResponsibleEvent", blank=True)
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
    """
    Модель для поддержки тегов на задачах с помощью taggit
    """
    content_object = ForeignKey('Task')


class Task(Model):
    """
    Модель задачи.
    """
    STATUS_CHOICES = (
        ('closed', 'Закрыто'),
        ('resolved', 'Готово'),
        ('in_progress', 'Выполняется'),
        ('open', 'Не назначено'),
        ('in_labor', 'На бирже'),
    )

    name = CharField("Название", max_length=50)
    responsible = ManyToManyField(User, verbose_name="Ответственные", related_name="tasks_responsible", blank=True)
    event = ForeignKey(Event, related_name="tasks", verbose_name="Мероприятие", blank=True, null=True)
    description = TextField("Описание", blank=True)
    tags = TaggableManager(through=TaggedTask, blank=True)
    hours_predict = FloatField("Расчётное количество часов",
                               validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
                               blank=False, null=False)
    number_of_assignees = PositiveSmallIntegerField("Количество людей", blank=False, null=False)
    candidates = ManyToManyField(User, verbose_name="Кандидаты", related_name="tasks_approve", blank=True)
    assignees = ManyToManyField(User, verbose_name="Назначенные", through="AssigneeTask", blank=True)
    rejected = ManyToManyField(User, verbose_name="Отклоненные", related_name="tasks_rejected", blank=True)
    datetime_created = DateTimeField("Время создания", default=timezone.now)
    datetime_limit = DateTimeField("Сроки", default=timezone.now)
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
        return str(self.name)


class AssigneeTask(Model):
    """
    Промежуточная модель задачи и назначанного юзера.
    """
    user = ForeignKey(User, verbose_name="Назначенный", related_name='participated')
    task = ForeignKey(Task, verbose_name="Задача", related_name='participants')
    hours = FloatField("Реальные часы", default=0.0,
                       validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    approved = BooleanField("Подтверждено", default=False)
    done = BooleanField("Готово", default=False)
    rewarded = BooleanField("Поощрено", default=False)

    def __str__(self):
        return str(self.user) + " in " + str(self.task)


class ResponsibleEvent(Model):
    """
    Промежуточная модель мероприятия и ответственного юзера.
    Для поддержки назанчения очков роста главами секторов по завершении мероприятия.
    """
    user = ForeignKey(User, verbose_name="Ответственный", related_name='event_responsible')
    event = ForeignKey(Event, verbose_name="Мероприятие", related_name='responsibles')
    done = BooleanField("Готово", default=False)

    def __str__(self):
        return str(self.user) + " in " + str(self.event)


class PointOperation(Model):
    """
    Модель очков роста
    """
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
        return str(self.timestamp) + ': ' + str(self.user.last_name) + '; ' + str(self.amount)


class TaskComment(Model):
    """
    Модель комментария для задач
    """
    user = ForeignKey(User, null=False, blank=False, related_name='task_comments', verbose_name="Юзер")
    task = ForeignKey(Task, related_name="comments", verbose_name="Задача", blank=False, null=False)
    datetime_created = DateTimeField("Время создания", default=timezone.now)
    datetime_last_modified = DateTimeField("Время последнего изменения", default=timezone.now)
    text = TextField("Текст комментария", blank=False)

    class Meta:
        verbose_name = "Комментарий к задаче"
        verbose_name_plural = "Комментарии к задаче"

    def get_absolute_url(self):
        return reverse('activism:task', kwargs={'pk': self.task.pk})

    def save(self, *args, **kwargs):
        self.datetime_last_modified = timezone.now()
        return super(TaskComment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.last_name) + ': ' + str(self.task.name) + ' ' + str(self.datetime_created)