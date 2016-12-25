from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.management import call_command
from accounts.models import PaymentsOperation, Profile
from activism.models import Sector, Event, Task


''' views test '''

class PaymentsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        call_command("create_groups")
        self.admin = User.objects.create_superuser(username='admin', password='admin', email='admin@l.ru')
        self.u1 = User.objects.create(username='111', password='111', email='111@l.ru')
        Profile.objects.create(user=self.u1, payments=0)
        Profile.objects.create(user=self.admin, payments=0)
        self.u1.groups.add(Group.objects.get(name="Активисты"))
        self.admin.groups.add(Group.objects.get(name="Ответственные за активистов"))
        self.client.login(username='admin', password='admin')
        self.numt = 0
        self.u1 = User.objects.get(pk=self.u1.pk)

    def create_and_close_task(self, user, time):
        r = self.client.post("/activism/tasks/create/", {'name': 'test' + str(self.numt), 'number_of_assignees': 1, 'hours_predict': time})
        t = Task.objects.get(name='test' + str(self.numt))
        self.client.post("/activism/tasks/" + str(t.pk) + '/', {'assignees_pk': user.pk})
        self.client.post("/activism/tasks/" + str(t.pk) + '/in_progress/')
        self.client.post("/activism/tasks/" + str(t.pk) + '/close/', {'hours_2': time})
        self.numt += 1

    def pay(self, const):
        self.client.post("/activism/payments/", {'const' : const})

    def test_payments(self):
        self.numt = 1
        self.create_and_close_task(self.u1, 41)
        self.pay(2)
        self.u1 = User.objects.get(pk=self.u1.pk)
        self.assertEqual(self.u1.profile.payments, 82)


