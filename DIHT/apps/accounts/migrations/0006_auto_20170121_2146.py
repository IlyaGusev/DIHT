# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0005_auto_20161031_0038'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentsOperation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('amount', models.IntegerField(verbose_name='Количество', default=0)),
                ('timestamp', models.DateTimeField(verbose_name='Дата', default=django.utils.timezone.now)),
                ('description', models.CharField(blank=True, null=True, max_length=150, verbose_name='Описание')),
                ('is_approved', models.BooleanField(verbose_name='Подтверждено', default=False)),
                ('moderator', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='moderated_paymentsoperations', null=True, verbose_name='Модератор')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='paymentsoperations', verbose_name='Юзер')),
            ],
            options={
                'verbose_name': 'Денежная операция поощрений',
                'verbose_name_plural': 'Денежные операции поощрений',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='payments',
            field=models.IntegerField(blank=True, null=True, verbose_name='Невыплачено поощрений', default=0),
        ),
        migrations.AlterField(
            model_name='moneyoperation',
            name='moderator',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='moderated_moneyoperations', null=True, verbose_name='Модератор'),
        ),
        migrations.AlterField(
            model_name='moneyoperation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='moneyoperations', verbose_name='Юзер'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pass_id',
            field=models.CharField(blank=True, unique=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('([0-9a-f]{2}){4,10}')], verbose_name='ID пропуска', default=None),
        ),
    ]
