from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from activism.models import Sector
import logging
logger = logging.getLogger('DIHT.custom')


class Command(BaseCommand):
    help = 'Creates sectors'

    def handle(self, *args, **options):

        colors = {"Проектный сектор": "9911dd",
                  "Информационный сектор": "07a0db",
                  "Хозяйственный сектор": "eeff00",
                  "Кураторский сектор": "00e900",
                  "Отдел по работе с абитуриентами": "fa0000"}

        for name, color in colors.items():
            Sector.objects.get_or_create(name=name, color=color)
        print("Done")
