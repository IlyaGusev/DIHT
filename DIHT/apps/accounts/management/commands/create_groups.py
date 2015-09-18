from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
import logging
logger = logging.getLogger('DIHT.custom')


class Command(BaseCommand):
    help = 'Creates groups'

    def handle(self, *args, **options):
        washing_cts = ContentType.objects.filter(app_label='washing')
        washing_perms = Permission.objects.filter(content_type__in=washing_cts).all()

        groups = [('Активисты', []),
                  ('Руководящая группа', []),
                  ('Ответственные за волонтёров', []),
                  ('Ответственные за стиралку', washing_perms),
                  ('Ответственные за работу с пользователями', []),
                  ('Ответственные за финансы', []),
                  ('Ответственные за качалку', []),
                  ]

        for g in groups:
            group, created = Group.objects.get_or_create(name=g[0])
            if created:
                for perm in g[1]:
                    group.permissions.add(perm)
                logger.info('Создана группа ' + g[0])
        print("Done")