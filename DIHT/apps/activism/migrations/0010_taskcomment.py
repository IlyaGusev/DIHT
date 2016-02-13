# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activism', '0009_auto_20151010_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('datetime_created', models.DateTimeField(verbose_name='Время создания', default=django.utils.timezone.now)),
                ('datetime_last_modified', models.DateTimeField(verbose_name='Время последнего изменения', default=django.utils.timezone.now)),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('task', models.ForeignKey(to='activism.Task', verbose_name='Задача', related_name='comments')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Юзер', related_name='task_comments')),
            ],
            options={
                'verbose_name': 'Комментарий к задаче',
                'verbose_name_plural': 'Комментарии к задаче',
            },
        ),
    ]
