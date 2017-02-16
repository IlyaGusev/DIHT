from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Profile, MoneyOperation
from washing.models import WashingMachine, WashingMachineRecord, RegularNonWorkingDay, NonWorkingDay, Parameters, BlackListRecord

''' views test '''


class CreateRecordTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='111',
                                             password='123456',
                                             first_name='Илья',
                                             last_name='Гусев',
                                             email='111@l.ru')
        Profile.objects.create(user=self.user,
                               money=200)
        BlackListRecord.objects.create(user=self.user,
                                       is_blocked=False)
        params = Parameters.objects.create(date=timezone.now().date(),
                                           delta_hour=5,
                                           delta_minute=0,
                                           start_hour=5,
                                           start_minute=0,
                                           price=100)
        self.user.save()
        self.machine = WashingMachine.objects.create(name="Machine1")
        self.machine.parameters.add(params)

    def test_create_record_ok(self):
        self.assertEqual(self.client.login(username='111', password='123456'), True)
        response = self.client.get('/washing/create_record/')
        self.assertTemplateUsed(response, 'washing/create_record.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/washing/create_record/', {'machine': self.machine.id,
                                                                'date': timezone.now().date().strftime("%d.%m.%Y"),
                                                                'time_from': '15:00',
                                                                'time_to': '20:00'})
        self.assertTemplateUsed(response, 'washing/create_record.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.moneyoperations.all().count(), 1)
        self.assertEqual(self.user.moneyoperations.all()[0].amount, -100)
        self.assertEqual(self.user.records.all().count(), 1)
        self.assertEqual(self.user.records.all()[0].machine.id, self.machine.id)