from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Avatar
from washing.models import BlackListRecord
import os
from DIHT.settings import BASE_DIR

class Command(BaseCommand):
    help = 'Creates groups'

    def handle(self, *args, **options):
        for user in User.objects.all():
            BlackListRecord.objects.get_or_create(user=user)
            Avatar.objects.get_or_create(user=user)
        print("Done")