# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activism', '0006_sector_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponsibleEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('done', models.BooleanField(verbose_name='Готово', default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='responsible',
        ),
        migrations.AddField(
            model_name='event',
            name='responsible',
            field=models.ManyToManyField(blank=True, verbose_name='Ответственные', to=settings.AUTH_USER_MODEL, through='activism.ResponsibleEvent'),
        ),
        migrations.AddField(
            model_name='responsibleevent',
            name='event',
            field=models.ForeignKey(verbose_name='Мероприятие', related_name='events', to='activism.Event'),
        ),
        migrations.AddField(
            model_name='responsibleevent',
            name='user',
            field=models.ForeignKey(verbose_name='Ответственный', related_name='event_responsible', to=settings.AUTH_USER_MODEL),
        ),
    ]
