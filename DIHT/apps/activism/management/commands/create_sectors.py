from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from activism.models import Sector
import logging
logger = logging.getLogger('DIHT.custom')

class Command(BaseCommand):
    help = 'Creates sectors'

    def handle(self, *args, **options):

        sectors = ['Проектный сектор',
                   'Отдел по работе с абитуриентами',
                   'Хозяйственный сектор',
                   'Кураторский сектор',
                   'Информационный сектор',
        ]
        for name in sectors:
            Sector.objects.get_or_create(name=name)
        print("Done")