# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssigneeTask',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('hours', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], blank=True, verbose_name='Реальные часы')),
                ('approved', models.BooleanField(default=False, verbose_name='Подтверждено')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Название', max_length=50)),
                ('date_created', models.DateField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('date_held', models.DateField(default=django.utils.timezone.now, verbose_name='Дата проведения')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('status', models.CharField(default='open', choices=[('closed', 'Проведено'), ('open', 'Готовится')], max_length=6, verbose_name='Статус')),
                ('assignees', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='events', blank=True, db_constraint='Ответственные')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Название', max_length=50)),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('main', models.ForeignKey(verbose_name='Руководитель', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': 'Сектор',
                'verbose_name_plural': 'Секторы',
            },
        ),
        migrations.CreateModel(
            name='TaggedTask',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Название', max_length=50)),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('hours_predict', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Расчётное количество часов')),
                ('number_of_assignees', models.PositiveSmallIntegerField(verbose_name='Количество людей')),
                ('datetime_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания')),
                ('datetime_limit', models.DateTimeField(default=django.utils.timezone.now, verbose_name='До какого времени надо сделать')),
                ('datetime_closed', models.DateTimeField(null=True, blank=True, verbose_name='Время закрытия')),
                ('datetime_last_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время последнего изменения')),
                ('status', models.CharField(default='open', choices=[('closed', 'Закрыто'), ('resolved', 'Готово'), ('in_progress', 'Выполняется'), ('open', 'Не назначено'), ('in_labor', 'На бирже')], max_length=15, verbose_name='Статус')),
                ('is_urgent', models.BooleanField(default=False, verbose_name='Срочное')),
                ('is_hard', models.BooleanField(default=False, verbose_name='Тяжёлое')),
                ('assignees', models.ManyToManyField(through='activism.AssigneeTask', to=settings.AUTH_USER_MODEL, blank=True, db_constraint='Назначенные')),
                ('candidates', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='tasks_approve', blank=True, db_constraint='Кандидаты')),
                ('creator', models.ForeignKey(verbose_name='Создатель', to=settings.AUTH_USER_MODEL, related_name='tasks_created')),
                ('event', models.ForeignKey(verbose_name='Мероприятие', null=True, to='activism.Event', related_name='tasks', blank=True)),
                ('rejected', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='tasks_rejected', blank=True, db_constraint='Отклоненные')),
                ('sector', models.ForeignKey(verbose_name='Сектор', null=True, to='activism.Sector', related_name='tasks', blank=True)),
                ('tags', taggit.managers.TaggableManager(through='activism.TaggedTask', to='taggit.Tag', help_text='A comma-separated list of tags.', blank=True, verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.AddField(
            model_name='taggedtask',
            name='content_object',
            field=models.ForeignKey(to='activism.Task'),
        ),
        migrations.AddField(
            model_name='taggedtask',
            name='tag',
            field=models.ForeignKey(to='taggit.Tag', related_name='activism_taggedtask_items'),
        ),
        migrations.AddField(
            model_name='event',
            name='sector',
            field=models.ForeignKey(verbose_name='Сектор', null=True, to='activism.Sector', related_name='events', blank=True),
        ),
        migrations.AddField(
            model_name='assigneetask',
            name='task',
            field=models.ForeignKey(verbose_name='Задача', to='activism.Task', related_name='participants'),
        ),
        migrations.AddField(
            model_name='assigneetask',
            name='user',
            field=models.ForeignKey(verbose_name='Назначенный', to=settings.AUTH_USER_MODEL, related_name='participated'),
        ),
    ]
