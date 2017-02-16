# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_auto_20161223_2231'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListRecord',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_blocked', models.BooleanField(default=False, verbose_name='Заблокирован в стиралке')),
                ('user', models.OneToOneField(related_name='black_list_record', verbose_name='Юзер', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Записи в чёрном списке',
                'verbose_name': 'Запись в чёрном списке',
            },
        ),
        migrations.CreateModel(
            name='NonWorkingDay',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
            ],
            options={
                'verbose_name_plural': 'Нерабочие дни',
                'verbose_name': 'Нерабочий день',
            },
        ),
        migrations.CreateModel(
            name='Parameters',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата начала действия')),
                ('delta_hour', models.PositiveSmallIntegerField(verbose_name='Промежуток времени(часы)')),
                ('delta_minute', models.PositiveSmallIntegerField(verbose_name='Промежуток времени(минуты)')),
                ('start_hour', models.PositiveSmallIntegerField(verbose_name='Время начала отсчёта промежутков(часы)')),
                ('start_minute', models.PositiveSmallIntegerField(verbose_name='Время начала отсчёта промежутков(минуты)')),
                ('price', models.PositiveSmallIntegerField(verbose_name='Цена за промежуток')),
                ('activist', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Наборы параметров',
                'verbose_name': 'Параметры',
            },
        ),
        migrations.CreateModel(
            name='RegularNonWorkingDay',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('day_of_week', models.PositiveSmallIntegerField(verbose_name='Номер дня недели, начиная с 0')),
            ],
            options={
                'verbose_name_plural': 'регулярные нерабочие дни',
                'verbose_name': 'Регулярный нерабочий день',
            },
        ),
        migrations.CreateModel(
            name='WashingMachine',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('parameters', models.ManyToManyField(related_name='machines', verbose_name='Параметры', to='washing.Parameters')),
            ],
            options={
                'verbose_name_plural': 'Стиральные машинки',
                'verbose_name': 'Стиральная машинка',
            },
        ),
        migrations.CreateModel(
            name='WashingMachineRecord',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('datetime_from', models.DateTimeField(verbose_name='Время начала')),
                ('datetime_to', models.DateTimeField(verbose_name='Время окончания')),
                ('machine', models.ForeignKey(related_name='records', verbose_name='Машинка', to='washing.WashingMachine')),
                ('money_operation', models.OneToOneField(related_name='washing_record', verbose_name='Денежная операция', to='accounts.MoneyOperation')),
                ('user', models.ForeignKey(related_name='records', verbose_name='Пользователь, занявший машинку', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['datetime_from'],
                'verbose_name_plural': 'Записи стиралки',
                'verbose_name': 'Запись стиралки',
            },
        ),
        migrations.AddField(
            model_name='regularnonworkingday',
            name='machine',
            field=models.ForeignKey(related_name='regular_non_working_days', verbose_name='Отключаемая машинка', to='washing.WashingMachine'),
        ),
        migrations.AddField(
            model_name='nonworkingday',
            name='machine',
            field=models.ForeignKey(related_name='non_working_days', verbose_name='Отключаемая машинка', to='washing.WashingMachine'),
        ),
    ]
