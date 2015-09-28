# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import django.utils.timezone

def set_colors(apps, schema_editor):
    colors = {
        "Проектный сектор": "9911dd",
        "Информационный сектор": "07a0db",
        "Хозяйственный сектор": "eeff00",
        "Кураторский сектор": "00e900",
        "Отдел по работе с абитуриентами": "fa0000",
    }

    Sector = apps.get_model("activism", "Sector")
    for name, color in colors.items():
        try:
            sector = Sector.objects.get(name=name)
            sector.color = color
            sector.save()
        except Sector.DoesNotExist:
            pass
        

class Migration(migrations.Migration):

    dependencies = [
        ('activism', '0005_auto_20150926_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='sector',
            name='color',
            field=models.CharField(validators=[django.core.validators.RegexValidator('[^0-9a-fA-F]', inverse_match=True)], default='aaaaaa', verbose_name='Цвет', max_length=6),
        ),
        migrations.RunPython(set_colors, lambda apps, schema_editor: None),
    ]
