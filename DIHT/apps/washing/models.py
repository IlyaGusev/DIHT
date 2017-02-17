from django.contrib.auth.models import User
from django.db.models import \
    PositiveSmallIntegerField, ForeignKey, DateTimeField, \
    DateField, BooleanField, OneToOneField,\
    Model, CharField, ManyToManyField
from accounts.models import MoneyOperation
from django.db import transaction


class Parameters(Model):
    """DAYS = (
        ('0', 'Понедельник'),
        ('1', 'Вторник'),
        ('2', 'Среда'),
        ('3', 'Четверг'),
        ('4', 'Пятница'),
        ('5', 'Суббота'),
        ('6', 'Воскресенье')
    )"""

    date = DateField("Дата начала действия")
    delta_hour = PositiveSmallIntegerField("Промежуток времени(часы)")
    delta_minute = PositiveSmallIntegerField("Промежуток времени(минуты)")
    start_hour = PositiveSmallIntegerField("Время начала отсчёта промежутков(часы)")
    start_minute = PositiveSmallIntegerField("Время начала отсчёта промежутков(минуты)")
    price = PositiveSmallIntegerField("Цена за промежуток")
    #activist = BooleanField("Для активистов", default=False)
    #activist_days = CharField("День начала работы стиралки(только для машинки на 1-м этаже)", max_length=2, choices=DAYS, null=True, blank=True)
    #activist_hours = PositiveSmallIntegerField("Количество времени работы(часы, только для машинки на 1-м этаже", null=True, blank=True)
    #activist_minutes = PositiveSmallIntegerField("Количество времени работы(минуты, только для машинки на 1-м этаже",
    #                                           null=True, blank=True)


    class Meta:
        verbose_name = "Параметры"
        verbose_name_plural = "Наборы параметров"

    def __str__(self):
        return 'Цена: ' + str(self.price) + \
               '; Промежуток: ' + str(self.delta_hour) + '-' + str(self.delta_minute) + \
               '; Начало: ' + str(self.start_hour) + '-' + str(self.start_minute)


class WashingMachine(Model):
    is_active = BooleanField("Активна", default=True)
    name = CharField("Название", max_length=50)
    parameters = ManyToManyField(Parameters, related_name='machines', verbose_name="Параметры", blank=False)

    class Meta:
        verbose_name = "Стиральная машинка"
        verbose_name_plural = "Стиральные машинки"

    def __str__(self):
        return self.name


class WashingMachineRecord(Model):
    machine = ForeignKey(WashingMachine, related_name='records', verbose_name="Машинка")
    user = ForeignKey(User, verbose_name="Пользователь, занявший машинку", related_name="records")
    datetime_from = DateTimeField("Время начала")
    datetime_to = DateTimeField("Время окончания")
    money_operation = OneToOneField(MoneyOperation, related_name='washing_record', verbose_name="Денежная операция")

    class Meta:
        ordering = ["datetime_from"]
        verbose_name = "Запись стиралки"
        verbose_name_plural = "Записи стиралки"

    @transaction.atomic
    def cancel(self):
        self.money_operation.cancel()
        self.delete()

    def __str__(self):
        return str(self.machine) + '; ' + str(self.user.last_name) + '; ' + str(self.datetime_from)


class RegularNonWorkingDay(Model):
    day_of_week = PositiveSmallIntegerField("Номер дня недели, начиная с 0")
    machine = ForeignKey(WashingMachine, related_name='regular_non_working_days', verbose_name="Отключаемая машинка")

    class Meta:
        verbose_name = "Регулярный нерабочий день"
        verbose_name_plural = "регулярные нерабочие дни"

    def __str__(self):
        return str(self.machine) + '; ' + str(self.day_of_week)


class NonWorkingDay(Model):
    date = DateField("Дата")
    machine = ForeignKey(WashingMachine, related_name='non_working_days', verbose_name="Отключаемая машинка")

    class Meta:
        verbose_name = "Нерабочий день"
        verbose_name_plural = "Нерабочие дни"

    def __str__(self):
        return str(self.machine) + '; ' + str(self.date)


class BlackListRecord(Model):
    user = OneToOneField(User, verbose_name="Юзер", related_name="black_list_record")
    is_blocked = BooleanField("Заблокирован в стиралке", default=False)

    class Meta:
        verbose_name = "Запись в чёрном списке"
        verbose_name_plural = "Записи в чёрном списке"

    def __str__(self):
        return str(self.user.username)
