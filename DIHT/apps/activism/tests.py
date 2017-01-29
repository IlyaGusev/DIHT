from django.test import LiveServerTestCase, TestCase, Client
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.management import call_command
from accounts.models import PaymentsOperation, Profile
from activism.models import Sector, Event, Task
from activism.utils import *
import datetime as dt
from time import sleep

''' views test '''

class PaymentsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        call_command("create_groups")
        self.admin = User.objects.create_superuser(username='admin', password='admin', email='admin@l.ru')
        self.u = []
        for i in range(1, 5):
            u = User.objects.create(username=str(i) * 3, password=str(i) * 3, email=(str(i) * 3) + '@l.ru')
            u.groups.add(Group.objects.get(name="Активисты"))
            u.save()
            Profile.objects.create(user=u, payments=0)
            self.u.append(User.objects.get(pk=u.pk))
        Profile.objects.create(user=self.admin, payments=0)
        self.admin.groups.add(Group.objects.get(name="Ответственные за активистов"))
        self.client.login(username='admin', password='admin')
        self.numt = 0

    def create_and_close_task(self, user, time, offset=0):
        r = self.client.post("/activism/tasks/create/", {'name': 'test' + str(self.numt), 'number_of_assignees': 1, 'hours_predict': time})
        t = Task.objects.get(name='test' + str(self.numt))
        self.client.post("/activism/tasks/" + str(t.pk) + '/', {'assignees_pk': user.pk})
        self.client.post("/activism/tasks/" + str(t.pk) + '/in_progress/')
        self.client.post("/activism/tasks/" + str(t.pk) + '/close/', {'hours_' + str(user.pk): time})
        t = Task.objects.get(pk = t.pk)
        t.datetime_closed = t.datetime_closed + dt.timedelta(offset)
        t.save()
        self.numt += 1

    def pay(self, const, begin_offset, end_offset):
        end = (timezone.now() + dt.timedelta(end_offset)).strftime('%Y-%m-%d')
        begin = (timezone.now() - dt.timedelta(begin_offset)).strftime('%Y-%m-%d')
        self.client.post("/activism/payments/", {'const' : const, 'begin' : begin, 'end' : end})
        for i in range(len(self.u)):
            self.u[i] = User.objects.get(pk=self.u[i].pk)


    def test_payments_1(self):
        self.create_and_close_task(self.u[1], 41)
        self.pay(2, 10, 10)
        self.assertEqual(self.u[1].profile.payments, 82)

    def test_payments_2(self):
        self.create_and_close_task(self.u[0], 39)
        self.pay(1, 10, 10)
        self.assertEqual(self.u[0].profile.payments, 0)
        self.create_and_close_task(self.u[0], 1)
        self.pay(1, -10, 20)
        self.assertEqual(self.u[0].profile.payments, 0)
        self.pay(2, 10, 10)
        self.assertEqual(self.u[0].profile.payments, 80)

    def test_level_up(self):
        user = self.u[1]
        self.create_and_close_task(user, 39, 1)
        self.assertEqual(get_level(user)['num'], 0)
        self.create_and_close_task(user, 1, 2)
        self.assertEqual(get_level(user)['num'], 1)

        self.create_and_close_task(user, 100, 3)
        self.create_and_close_task(user, 19, 4)
        self.assertEqual(get_level(user)['num'], 1)
        self.create_and_close_task(user, 1, 5)
        self.assertEqual(get_level(user)['num'], 2)

        self.create_and_close_task(user, 100, 6)
        self.create_and_close_task(user, 89, 7)
        self.assertEqual(get_level(user)['num'], 2)
        self.create_and_close_task(user, 1, 8)
        self.assertEqual(get_level(user)['num'], 3)

        self.create_and_close_task(user, 100, 9)
        self.create_and_close_task(user, 100, 10)
        self.create_and_close_task(user, 100, 11)
        self.create_and_close_task(user, 49, 12)
        self.assertEqual(get_level(user)['num'], 3)
        self.create_and_close_task(user, 1, 13)
        self.assertEqual(get_level(user)['num'], 4)
        self.pay(10, 23, 23)
        self.assertEqual(user.profile.payments, 39 * 10 + 120 * 10 + 190 * 17 + 350 * 24 + 10 * 4)


