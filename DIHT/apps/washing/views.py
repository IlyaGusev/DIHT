from django.views.generic import TemplateView, View
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from washing.models import WashingMachine, WashingMachineRecord, RegularNonWorkingDay, NonWorkingDay, Parameters
from accounts.models import MoneyOperation
import collections
import datetime as dt
import pytz
import logging
logger = logging.getLogger('DIHT.custom')

week = ['Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота',
        'Воскресенье']


class IndexView(TemplateView):
    template_name = 'washing/washing.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['charge_washing'] = Group.objects.get(name=u'Ответственные за стиралку').user_set.all()
        machines = WashingMachine.objects.all()
        current = dt.datetime.now(tz=pytz.timezone('Europe/Moscow'))

        schedule = collections.OrderedDict()

        day = current.date()
        for i in range(7):
            schedule[day] = collections.OrderedDict()
            for machine in machines:
                machine_params = machine.parameters.all().filter(date__lte=day).order_by('-date')
                if machine_params.count() > 0:
                    params = machine_params[0]

                    times = (24 * 60 - params.start_minute - params.start_hour * 60) // \
                            (params.delta_minute + params.delta_hour * 60)

                    start = params.start_hour * 60 + params.start_minute
                    delta = params.delta_hour * 60 + params.delta_minute
                    for j in range(times):
                        start_hour = start//60
                        start_minute = start - start_hour * 60
                        end_hour = (start + delta)//60
                        end_minute = start + delta - end_hour * 60
                        d = dt.datetime.combine(day, dt.time(start_hour, start_minute, 0))

                        status = 'OK'
                        if machine.regular_non_working_days.filter(day_of_week=day.weekday()).count() > 0:
                            status = 'DISABLE'
                        if machine.non_working_days.filter(date=day).count() > 0:
                            status = 'DISABLE'
                        if machine.records.filter(datetime_from=d).count() > 0:
                            if machine.records.get(datetime_from=d).user == self.request.user:
                                status = "YOURS"
                            else:
                                status = "BUSY"

                        interval = (dt.time(start_hour, start_minute, 0),
                                    dt.time(end_hour, end_minute, 0))
                        if schedule[day].get(interval) is None:
                            schedule[day][interval] = collections.OrderedDict()
                        schedule[day][interval][machine] = status
                        start += delta

            day += dt.timedelta(days=1)
        context['week'] = week
        context['schedule'] = schedule
        context['machines'] = machines
        return context


def parse_record(request):
    date = request.POST['date']
    time_from = request.POST['time_from']
    time_to = request.POST['time_to']
    machine = WashingMachine.objects.get(id=request.POST['machine'])
    user = request.user
    datetime_from = dt.datetime.strptime(date+' '+time_from, '%d.%m.%Y %H:%M')
    datetime_to = dt.datetime.strptime(date+' '+time_to, '%d.%m.%Y %H:%M')
    return {'machine': machine, 'user': user, 'datetime_from': datetime_from, 'datetime_to': datetime_to}


class CreateRecordView(TemplateView):
    template_name = "washing/create_record.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateRecordView, self).dispatch(*args, **kwargs)

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        record = parse_record(request)
        price = record['machine'].parameters.all().filter(date__lte=record['datetime_from'].date()).order_by('-date')[0].price
        operation = MoneyOperation.objects.create(user=record['user'],
                                                  amount=-price,
                                                  timestamp=dt.datetime.now(),
                                                  description="Стиралка")
        WashingMachineRecord.objects.create(machine=record['machine'],
                                            user=record['user'],
                                            datetime_from=record['datetime_from'],
                                            datetime_to=record['datetime_to'],
                                            money_operation=operation)
        return super(CreateRecordView, self).get(request, *args, **kwargs)


class CancelRecordView(TemplateView):
    template_name = "washing/cancel_record.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CancelRecordView, self).dispatch(*args, **kwargs)

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        record = parse_record(request)
        record_obj = WashingMachineRecord.objects.get(machine=record['machine'],
                                                      user=record['user'],
                                                      datetime_from=record['datetime_from'],
                                                      datetime_to=record['datetime_to'])
        # record_obj.money_operation.cancel()
        record_obj.delete()
        return super(CancelRecordView, self).get(request, *args, **kwargs)