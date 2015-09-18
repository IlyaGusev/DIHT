from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Avatar
from washing.models import BlackListRecord
from django.core.files import File
import os
from DIHT.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Fills empty models'

    def handle(self, *args, **options):
        for user in User.objects.all():
            BlackListRecord.objects.get_or_create(user=user)
            avatar = Avatar.objects.get_or_create(user=user)
            if not avatar[0].img:
                with open(os.path.join(BASE_DIR, 'DIHT/static/img/standart_avatar.png'), 'rb') as img_file:
                    avatar[0].img.save("avatar", File(img_file), save=True)
                avatar[0].save()
        print("Done")