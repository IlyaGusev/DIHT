# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания: 04/08/2015
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Тесты модуля accounts. Их недостаточно, нужно больше.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from accounts.models import Profile, MoneyOperation

''' models test'''


class MoneyOperationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='111', password='111', email='111@l.ru')
        Profile.objects.create(user=self.user, money=0)

    def test_money_operation(self):
        op1 = MoneyOperation.objects.create(user=self.user, amount=100, timestamp=timezone.now())
        self.assertTrue(isinstance(op1, MoneyOperation))
        self.assertEqual(self.user.profile.money, op1.amount)
        op2 = MoneyOperation.objects.create(user=self.user, amount=100, timestamp=timezone.now())
        self.assertEqual(self.user.profile.money, op1.amount + op2.amount)
        op1.cancel()
        self.assertEqual(self.user.profile.money, op2.amount)
        op2.cancel()
        self.assertEqual(self.user.profile.money, 0)


''' views test '''


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_ok = {
            'username': 'yallen',
            'password': '123456',
            'password_repeat': '123456',
            'first_name': 'Илья',
            'last_name': 'Гусев',
            'middle_name': 'Олегович',
            'email': 'yallen@gmail.com',
            'sex': False,
            'hostel': '2',
            'room_number': '111',
            'group_number': '492',
            'mobile': '+79259999999',
        }
        User.objects.create(username='valid_username', password='111', email='111@l.ru')

    def test_register_ok(self):
        response = self.client.get('/accounts/signup/')
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/accounts/signup/', self.user_ok)
        self.assertRedirects(response, '/accounts/signup_ok/', status_code=302, target_status_code=200)
        user = User.objects.get(username=self.user_ok['username'])
        self.assertTrue(isinstance(user, User))

        response = self.client.get('/accounts/signup_ok/')
        self.assertTemplateUsed(response, 'accounts/signup_ok.html')
        self.assertEqual(response.status_code, 200)

    def test_register_username(self):
        usernames = ['ffff', '3ffff', 'fffdsdfa*']
        for username in usernames:
            user = self.user_ok
            user['username'] = username
            response = self.client.post('/accounts/signup/', user)
            self.assertFormError(response, 'form', 'username', ['Некорректный логин.'])

        user = self.user_ok
        user['username'] = 'valid_username'
        response = self.client.post('/accounts/signup/', user)
        self.assertFormError(response, 'form', 'username', ['Логин уже используется.'])

    def test_register_email(self):
        emails = ['wwwwww', 'wwwww@dfdsfa', 'fdsaf.com', '@dfssad.ru']
        for email in emails:
            user = self.user_ok
            user['email'] = email
            response = self.client.post('/accounts/signup/', user)
            self.assertFormError(response, 'form', 'email', ['Введите правильный адрес электронной почты.'])

    def test_register_names(self):
        names = ['dfsdfa', 'Dfdsfasd', 'авыаф', 'вафвыаыфё']
        for name in names:
            user = self.user_ok
            user['first_name'] = name
            user['last_name'] = name
            user['middle_name'] = name
            response = self.client.post('/accounts/signup/', user)
            self.assertFormError(response, 'form', 'first_name',
                                 ['Неверный формат имени: первыя буква должна быть заглавной, допустимы только русские символы.'])
            self.assertFormError(response, 'form', 'last_name',
                                 ['Неверный формат фамилии: первыя буква должна быть заглавной, допустимы только русские символы.'])
            self.assertFormError(response, 'form', 'middle_name',
                                 ['Неверный формат отчества: первыя буква должна быть заглавной, допустимы только русские символы.'])

    def test_register_password(self):
        passwords = ["12345", '12345678901234567890123456erewa7890']
        for password in passwords:
            user = self.user_ok
            user['password'] = password
            response = self.client.post('/accounts/signup/', user)
            self.assertFormError(response, 'form', 'password', ['Неверная длина пароля.'])

    def test_register_password_repeat(self):
        user = self.user_ok
        user['password_repeat'] += '1'
        response = self.client.post('/accounts/signup/', user)
        self.assertFormError(response, 'form', 'password_repeat', ["Пароли не совпадают."])

    def test_register_mobile(self):
        mobiles = ['8999999999', '+71231312', '+99250000111']
        for mobile in mobiles:
            user = self.user_ok
            user['mobile'] = mobile
            response = self.client.post('/accounts/signup/', user)
            self.assertFormError(response, 'form', 'mobile', ['Некорректный номер телефона.'])


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create(username='111', password='111', email='111@l.ru')

    def test_login_ok(self):
        response = self.client.post('/accounts/login/', {'username': '111', 'password': '111'})
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(response.status_code, 200)

    def test_login_errors(self):
        response = self.client.post('/accounts/login/', {'username': '111', 'password': '222'})
        self.assertFormError(response, 'form', None,
                             ['Пожалуйста, введите правильные имя пользователя и пароль. '
                              'Оба поля могут быть чувствительны к регистру.'])
        response = self.client.post('/accounts/login/', {'username': '222', 'password': '222'})
        self.assertFormError(response, 'form', None,
                             ['Пожалуйста, введите правильные имя пользователя и пароль. '
                              'Оба поля могут быть чувствительны к регистру.'])