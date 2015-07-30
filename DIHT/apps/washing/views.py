from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from washing.models import WashingMachine, WashingMachineRecord, RegularNonWorkingDay, NonWorkingDay, Parameters
import collections
import datetime as dt
import pytz
import logging
logger = logging.getLogger('DIHT.custom')

week = ['Воскресенье',
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота']

class IndexView(TemplateView):
    template_name = 'washing/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['charge_washing'] = Group.objects.get(name=u'Ответственные за стиралку').user_set.all()
        machines = WashingMachine.objects.all()
        current = dt.datetime.now(tz=pytz.timezone('Europe/Moscow'))

        schedule = collections.OrderedDict()

        current_day = current.date()
        for i in range(7):
            day = str(current_day)+' ('+week[current_day.weekday()]+')'
            schedule[day] = collections.OrderedDict()
            for machine in machines:
                machine_params = machine.parameters.all().filter(date__lte=current_day).order_by('-date')
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
                        d = dt.datetime.combine(current_day, dt.time(start_hour, start_minute, 0))

                        status = 'OK'
                        if machine.regular_non_working_days.filter(day_of_week=current_day.weekday()).count() > 0:
                            status = 'DISABLE'
                        if machine.non_working_days.filter(date=current_day).count() > 0:
                            status = 'DISABLE'
                        if machine.records.filter(datetime_from=d).count() > 0:
                            if machine.records.get(datetime_from=d).user == self.request.user:
                                status = "YOURS"
                            else:
                                status = "BUSY"

                        interval = ("%0.2d" % start_hour)+':'+("%0.2d" % start_minute)+'-' +\
                                   ("%0.2d" % end_hour)+':'+("%0.2d" % end_minute)
                        if schedule[day].get(interval) is None:
                            schedule[day][interval] = collections.OrderedDict()
                        schedule[day][interval][machine.name] = status
                        start += delta

            current_day += dt.timedelta(days=1)
        context['schedule'] = schedule
        context['machines'] = machines
        return context

