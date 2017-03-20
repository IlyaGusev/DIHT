import datetime as dt
import logging
from collections import OrderedDict

from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group, User
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseForbidden
from django.conf import settings
from washing.models import WashingMachine, WashingMachineRecord, RegularNonWorkingDay, NonWorkingDay, Parameters
from accounts.models import Profile, MoneyOperation
from braces.views import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from activism.models import PointOperation

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

    def create_intervals(self, machine, machine_params, day, times):
        start = machine_params.start_hour * 60 + machine_params.start_minute
        delta = machine_params.delta_hour * 60 + machine_params.delta_minute
        result = OrderedDict()
        for j in range(times):
            start_hour = start // 60
            start_minute = start - start_hour * 60
            end_hour = (start + delta) // 60 % 24
            end_minute = (start + delta - end_hour * 60) % 60
            if start_hour >= 24:
                day += dt.timedelta(days=start_hour // 24)
                start_hour %= 24
            d = dt.datetime.combine(day, dt.time(start_hour, start_minute, 0))

            status = 'OK'
            user = self.request.user
            if machine.regular_non_working_days.filter(day_of_week=day.weekday()).exists():
                status = 'DISABLE'
            if machine.non_working_days.filter(date=day).exists():
                status = 'DISABLE'
            if machine.records.filter(datetime_from=d).exists():
                if machine.records.get(datetime_from=d).user == self.request.user:
                    status = "YOURS"
                else:
                    status = "BUSY"
                user = machine.records.get(datetime_from=d).user

            interval = (dt.time(start_hour, start_minute, 0),
                        dt.time(end_hour, end_minute, 0))
            result.setdefault(interval, OrderedDict())[machine] = [status, machine_params.price, user, True]
            start += delta
        return result

    def get_context_data(self, **kwargs):
        is_activist = False
        if self.request.user.is_anonymous():
            OPcount = 0
        else:
            OPcount = self.request.user.pointoperations.aggregate(Sum('amount'))['amount__sum']
        if self.request.POST:
            if self.request.POST.get('activist') and (OPcount >= 16 or self.request.user.groups.filter(name__in=["Руководящая группа"]).exists()):
                is_activist = True

        context = super(IndexView, self).get_context_data(**kwargs)
        if Group.objects.filter(name='Ответственные за стиралку').exists():
            context['charge_washing'] = Group.objects.get(name='Ответственные за стиралку').user_set.all()
        machines = WashingMachine.objects.filter(is_active=True, parameters__activist=is_activist).order_by('name')

        schedule = OrderedDict()
        day = timezone.now().date()
        context['current'] = day

        if is_activist:
            machine = machines[0]
            machine_params = machine.parameters.filter(date__lte=day).order_by('-date').first()
            while day.weekday() != int(machine_params.activist_days):
                if day.weekday() == (int(machine_params.activist_days) + 1) % 7 \
                        and (machine_params.start_hour + machine_params.activist_hours) % 24 >= dt.datetime.now().hour\
                        and machine_params.start_hour + machine_params.activist_hours >= 24:
                    day -= dt.timedelta(days=1)
                    break
                day += dt.timedelta(days=1)
            end_work_day = day + dt.timedelta(hours=machine_params.activist_hours + machine_params.start_hour,
                                              minutes=machine_params.activist_minutes+machine_params.start_minute)
            end_work_hour = (machine_params.start_hour + machine_params.activist_hours) % 24
            end_work_minute = (machine_params.start_minute + machine_params.activist_minutes) % 60
            if end_work_minute < machine_params.start_minute:
                end_work_hour += 1
            firstday = day
            while True:
                schedule[day] = OrderedDict()
                if day == end_work_day:
                    times = (end_work_hour * 60 + end_work_minute) // \
                        (machine_params.delta_minute + machine_params.delta_hour * 60)
                elif day == firstday:
                    times = (24 * 60 - machine_params.start_minute - machine_params.start_hour * 60) // \
                            (machine_params.delta_minute + machine_params.delta_hour * 60)
                else:
                    times = 24 * 60 // (machine_params.delta_minute + machine_params.delta_hour * 60)
                if day != firstday:
                    machine_params.start_hour = machine_params.start_minute = 0

                schedule[day] = self.create_intervals(machine, machine_params, day, times)
                if not schedule[day]:
                    del schedule[day]
                if day == end_work_day:
                    break
                else:
                    day += dt.timedelta(days=1)
        else:
            for i in range(7):
                schedule[day] = OrderedDict()
                for machine in machines:
                    machine_params = machine.parameters.all().filter(date__lte=day).order_by('-date').first()

                    times = (24 * 60 - machine_params.start_minute - machine_params.start_hour * 60) // \
                            (machine_params.delta_minute + machine_params.delta_hour * 60)

                    machine_schedule = self.create_intervals(machine, machine_params, day, times)
                    schedule.setdefault(day, OrderedDict)
                    for interval in machine_schedule:
                        schedule[day].setdefault(interval, OrderedDict()).update(machine_schedule[interval])
                day += dt.timedelta(days=1)
        context['week'] = week
        context['schedule'] = schedule
        context['machines'] = machines
        if self.request.POST:
            return render(self.request, self.template_name, context)
        return context

    def post(self, request, *args, **kwargs):
        op = 0
        if 'cancel_id' in self.request.POST:
            user_id = self.request.POST.get("cancel_id")
            record = parse_record(request)
            record_obj = WashingMachineRecord.objects.get(machine=record['machine'],
                                                          user=User.objects.get(id=int(user_id)),
                                                          datetime_from=record['datetime_from'],
                                                          datetime_to=record['datetime_to'])
            if request.user.groups.filter(name__in=["Ответственные за активистов"]).exists():
                record_obj.money_operation.cancel()
                record_obj.delete()
            return IndexView.get_context_data(self, **kwargs)
        if 'check_op' in self.request.POST and self.request.POST.get('check_op'):
            for x in PointOperation.objects.filter(user=self.request.user.id):
                op += x.amount
            if (op < 16 or request.user.groups.filter(name__in=["Руководящая группа"])) \
                    and not request.user.groups.filter(name__in=["Ответственные за активистов"]).exists():
                return HttpResponse("false")
        if not ('check_op' in self.request.POST and self.request.POST.get('check_op') == 'continue'):
            kwargs['op'] = op
            return IndexView.get_context_data(self, **kwargs)
        return HttpResponse("true")


def parse_record(request):
    date = request.POST['date']
    time_from = request.POST['time_from']
    time_to = request.POST['time_to']
    machine = WashingMachine.objects.get(id=request.POST['machine'])
    datetime_from = dt.datetime.strptime(date + ' ' + time_from, '%d.%m.%Y %H:%M')
    datetime_to = dt.datetime.strptime(date + ' ' + time_to, '%d.%m.%Y %H:%M')
    return {'machine': machine, 'datetime_from': datetime_from, 'datetime_to': datetime_to}


# TODO: validate datetime_to
class CreateRecordView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "washing/create_record.html"
    raise_exception = True

    def test_func(self, user):
        return (not hasattr(user, 'black_list_record')) or (not user.black_list_record.is_blocked)

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        record = parse_record(request)
        if WashingMachineRecord.objects.filter(machine=record['machine']).filter(datetime_from=record['datetime_from']).exists():
            return JsonResponse({"no_money": "Эта стиралка уже занята"}, status=400)
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
            return JsonResponse({"no_money": "Нет денег для оплаты, пополните у ответственных за стиралку/финансы"}, status=400)
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


class VirtualBlockDayView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "washing/block_day.html"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(VirtualBlockDayView, self).get_context_data(**kwargs)
        machines = WashingMachine.objects.filter(is_active=True)
        context['machines'] = machines
        return context


def parse_block(request):
    machine_id = request.POST['machine']
    if machine_id == 'all':
        machines = WashingMachine.objects.filter(is_active=True)
    else:
        machines = WashingMachine.objects.filter(id=machine_id)
    date = request.POST['date']
    return machines, date


class BlockDayView(VirtualBlockDayView):
    permission_required = "washing.add_nonworkingday"

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        machines, date = parse_block(request)
        for machine in machines:
            NonWorkingDay.objects.create(date=dt.datetime.strptime(date, '%d.%m.%Y').date(), machine=machine)
        return super(BlockDayView, self).get(request, *args, **kwargs)


class UnblockDayView(VirtualBlockDayView):
    permission_required = 'washing.delete_nonworkingday'

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        machines, date = parse_block(request)
        for machine in machines:
            NonWorkingDay.objects.filter(date=dt.datetime.strptime(date, '%d.%m.%Y').date(), machine=machine).delete()
        return super(UnblockDayView, self).get(request, *args, **kwargs)

#TODO: Использовать class-based method_decorator из Django 1.9, чтобы не переопределять dispatch
class CheckAccessView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CheckAccessView, self).dispatch(request, *args, **kwargs)

    def post(self, request, uid, *args, **kwargs):
        takeaway_time = dt.timedelta(1) # one day to take away clothes

        if "secret" not in request.POST or request.POST['secret'] != settings.ACCESS_SECRET:
            return HttpResponseForbidden()

        now = dt.datetime.now()
        user_query = Profile.objects.filter(pass_id=uid.lower())
        if user_query.exists() and WashingMachineRecord.objects.filter(
                datetime_from__lte=now,
                datetime_to__gte=now - takeaway_time,
                user=user_query.get().user
                ).exists():
            return HttpResponse("GRANTED")
        else:
            return HttpResponse("DENIED")

