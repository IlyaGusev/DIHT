import collections
import datetime as dt
import logging
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from washing.models import WashingMachine, WashingMachineRecord, RegularNonWorkingDay, NonWorkingDay, Parameters
from accounts.models import MoneyOperation
from braces.views import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

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
        machines = WashingMachine.objects.filter(is_active=True)
        current = timezone.now()

        schedule = collections.OrderedDict()

        day = current.date()
        context['current'] = day
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
                        schedule[day][interval][machine] = (status, params.price)
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
    datetime_from = dt.datetime.strptime(date+' '+time_from, '%d.%m.%Y %H:%M')
    datetime_to = dt.datetime.strptime(date+' '+time_to, '%d.%m.%Y %H:%M')
    return {'machine': machine, 'datetime_from': datetime_from, 'datetime_to': datetime_to}


class CreateRecordView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "washing/create_record.html"
    raise_exception = True

    def test_func(self, user):
        return not user.black_list_record.is_blocked

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        record = parse_record(request)
        price = record['machine'].parameters.all().filter(date__lte=record['datetime_from'].date()).order_by('-date')[0].price
        if request.user.profile.money >= price:
            operation = MoneyOperation.objects.create(user=request.user,
                                                      amount=-price,
                                                      timestamp=timezone.now(),
                                                      description="Стиралка")
            WashingMachineRecord.objects.create(machine=record['machine'],
                                                user=request.user,
                                                datetime_from=record['datetime_from'],
                                                datetime_to=record['datetime_to'],
                                                money_operation=operation)
        else:
            return JsonResponse({"no_money": "Нет денег для оплаты"}, status=400)
        return super(CreateRecordView, self).get(request, *args, **kwargs)


class CancelRecordView(LoginRequiredMixin, TemplateView):
    template_name = "washing/cancel_record.html"
    raise_exception = True

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        record = parse_record(request)
        record_obj = WashingMachineRecord.objects.get(machine=record['machine'],
                                                      user=request.user,
                                                      datetime_from=record['datetime_from'],
                                                      datetime_to=record['datetime_to'])
        record_obj.money_operation.cancel()
        record_obj.delete()
        return super(CancelRecordView, self).get(request, *args, **kwargs)


class BlockDayView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "washing/block_day.html"
    permission_required = "washing.add_nonworkingday"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(BlockDayView, self).get_context_data(**kwargs)
        machines = WashingMachine.objects.filter(is_active=True)
        context['machines'] = machines
        return context

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        machine_id = request.POST['machine']
        if machine_id == 'all':
            machines = WashingMachine.objects.filter(is_active=True)
        else:
            machines = WashingMachine.objects.filter(id=machine_id)
        date = request.POST['date']
        for machine in machines:
            NonWorkingDay.objects.create(date=dt.datetime.strptime(date, '%d.%m.%Y').date(), machine=machine)
        return super(BlockDayView, self).get(request, *args, **kwargs)


class UnblockDayView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "washing/block_day.html"
    permission_required = 'washing.delete_nonworkingday'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(UnblockDayView, self).get_context_data(**kwargs)
        machines = WashingMachine.objects.filter(is_active=True)
        context['machines'] = machines
        return context

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        machine_id = request.POST['machine']
        if machine_id == 'all':
            machines = WashingMachine.objects.filter(is_active=True)
        else:
            machines = WashingMachine.objects.filter(id=machine_id)
        date = request.POST['date']
        for machine in machines:
            NonWorkingDay.objects.filter(date=dt.datetime.strptime(date, '%d.%m.%Y').date(), machine=machine).delete()
        return super(UnblockDayView, self).get(request, *args, **kwargs)