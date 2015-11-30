# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_moneyoperation_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Описание')),
                ('owner', models.ForeignKey(related_name='keys', verbose_name='Владелец', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Ключи',
                'verbose_name': 'Ключ',
            },
        ),
        migrations.CreateModel(
            name='KeyTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('first_owner', models.ForeignKey(related_name='keys_first', verbose_name='От кого', to=settings.AUTH_USER_MODEL)),
                ('key', models.ForeignKey(related_name='transfers', verbose_name='Передачи', to='accounts.Key')),
                ('second_owner', models.ForeignKey(related_name='keys_second', verbose_name='К кому', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Передачи ключа',
                'verbose_name': 'Передача ключа',
            },
        ),
    ]
