# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания:
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Самый главный файл - логика, связанная с активистами.
        Клиентская часть в activism.js и activism/*.js
        3 вида views - страница, действие, модаль (всплывающее окно).
        Все модали работают с common.js. Если видишь JSON - это туда.
"""
import datetime as dt
from itertools import chain
from collections import OrderedDict
from copy import deepcopy
from django.db.models import Count
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, View, CreateView, TemplateView, DetailView, DeleteView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.utils import timezone
from braces.views import LoginRequiredMixin, GroupRequiredMixin, UserPassesTestMixin
from reversion import get_for_object
from activism.models import Event, Task, AssigneeTask, Sector, PointOperation, ResponsibleEvent, TaskComment
from activism.forms import TaskForm, EventForm, TaskCreateForm, PointForm, TaskCommentForm
from activism.utils import global_checks, get_level, get_level_by_num
from accounts.models import PaymentsOperation
from django.db.models import Sum
import math
import csv

"""
    Mixins
"""


class PostAccessMixin(SingleObjectMixin):
    """
    Mixin для проверки прав. От UserPassesTestMixin отличается тем, что работает только с POST частью.
    """
    def post(self, request, *args, **kwargs):
        checks = global_checks(request.user, self.get_object())
        if checks['is_responsible'] or checks['can_all'] or checks['is_main']:
            return super(PostAccessMixin, self).post(request, args, kwargs)
        else:
            raise PermissionDenied


class DefaultContextMixin(object):
    """
    Mixin для введения общего конекста.
    """
    def get_context_data(self, **kwargs):
        context = super(DefaultContextMixin, self).get_context_data(**kwargs)
        user = self.request.user
        context['events'] = Event.objects.all()
        context['sectors'] = Sector.objects.all()
        context['users'] = User.objects.all()
        obj = self.get_object() if hasattr(self, 'object') else None
        context.update(global_checks(user, obj))
        return context


class JsonCreateMixin(object):
    """
    Mixin для внедрения при создании объекта.
    Автоматически назначает текущего пользователя ответственным и возвращает JSON.
    """
    def form_valid(self, form):
        result = super(JsonCreateMixin, self).form_valid(form)
        if not isinstance(form.instance, Event):
            form.instance.responsible.add(self.request.user)
        else:
            ResponsibleEvent.objects.create(event=form.instance, user=self.request.user)
        return JsonResponse({'url': result.url}, status=200)


class JsonErrorsMixin(object):
    """
    Mixin для правильной обработки ошибок в модальных формах.
    Клентская часть в common.js, функция view_modal_errors.
    """
    def form_invalid(self, form):
        super(JsonErrorsMixin, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


"""
    Action views
"""


class UnlockView(LoginRequiredMixin, View):
    """
    Действие для открытия доступа к модулю.
    """
    raise_exception = True

    def get(self, request, *args, **kwargs):
        user = request.user
        user.groups.add(Group.objects.get(name="Активисты"))
        return HttpResponseRedirect(reverse('activism:index'))


class EventCreateView(LoginRequiredMixin, GroupRequiredMixin, JsonCreateMixin, JsonErrorsMixin, CreateView):
    """
    Модаль для создания мероприятия.
    """
    model = Event
    template_name = 'activism/event_create.html'
    fields = ('name', 'sector')
    group_required = ["Руководящая группа", "Ответственные за активистов"]
    raise_exception = True


# EventClosingView  - begin
"""
    Действие закрытия мероприятия.
    Такая сложная логика из-за требования руководителей секторов назначать ОР по завершении мероприятия
    и разрешать конфликты.
    Из-за большого объёма разбито на методы.
"""


def get_event_assignees(event):
    assignees = set()
    for task in Task.objects.filter(event=event.pk):
        assignees = assignees.union(set(task.assignees.all()))
    return list(assignees)


def check_user_can_create_gp(user):
    checks = global_checks(user)
    return checks['is_main'] or checks['can_all']


def check_event_closing(event):
    assignees = get_event_assignees(event)
    has_main = False
    all_done = True
    has_conflicts = False
    only_main_gp = True
    for u in [User.objects.get(pk=i) for i in ResponsibleEvent.objects.filter(event=event)
                                                              .values_list('user', flat=True)]:
        if Group.objects.get(name="Руководящая группа") in u.groups.all():
            has_main = True

    for entity in ResponsibleEvent.objects.filter(event=event):
        if (has_main and
            Group.objects.get(name="Руководящая группа") in entity.user.groups.all() and
            not entity.done) or \
           (not has_main and not entity.done):
            all_done = False

    for assignee in assignees:
        op = PointOperation.objects.filter(user=assignee, description="За " + event.name)
        if op.count() > 1:
            has_conflicts = True
        elif op.exists():
            if not check_user_can_create_gp(op[0].moderator):
                only_main_gp = False

    return {"all_done": all_done,
            "only_main_gp": only_main_gp,
            "has_conflicts": has_conflicts,
            "all_ok": all_done and only_main_gp and not has_conflicts}


def create_point_op(request, assignee, event, user):
    gp = request.POST.get("gp_"+str(assignee.pk))
    if gp is not None and gp != '':
        if 0 < int(gp) < 3:
            PointOperation.objects.create(user=assignee, amount=int(gp), timestamp=timezone.now(),
                                          description="За " + event.name, moderator=user)


class EventCloseView(GroupRequiredMixin, LoginRequiredMixin, DefaultContextMixin, DetailView):
    model = Event
    group_required = "Активисты"
    template_name = "activism/event_close.html"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(EventCloseView, self).get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user
        gps = {}
        assignees = get_event_assignees(event)
        # Заполняем таблицу ОР назначенных и вливаем её в контекст
        for assignee in assignees:
            op = assignee.pointoperations.filter(description="За "+event.name, moderator=user)
            if op.exists():
                gps[assignee.pk] = op[0]
        context['assignees'] = assignees
        context['gps'] = gps

        # Если юзер ответственный за активистов или суперюзер,
        # он может видеть всю таблицу от всех ответственных с конфликтами
        if context['can_all']:
            gp_table = OrderedDict()
            ordered_assignees = OrderedDict()
            for responsible in event.responsible.all():
                ordered_assignees[responsible] = 0
            # Заполняем gp_table
            for assignee in assignees:
                gp_table[assignee] = deepcopy(ordered_assignees)
                for responsible in event.responsible.all():
                    gps = PointOperation.objects.filter(user=assignee, moderator=responsible,
                                                        description="За " + event.name)
                    if gps.exists():
                        gp_table[assignee][responsible] = gps[0].amount
            conflict_users = PointOperation.objects.filter(description="За "+event.name)\
                                                   .values('user')\
                                                   .annotate(Count('id')).order_by()\
                                                   .filter(id__count__gt=1)\
                                                   .values_list('user', flat=True)
            #
            not_main_users = []
            for assignee in assignees:
                op = PointOperation.objects.filter(user=assignee, description="За " + event.name)
                if op.count() == 1 and not check_user_can_create_gp(op[0].moderator):
                    not_main_users.append(assignee.id)
            responsible = OrderedDict()
            for res in ordered_assignees.keys():
                responsible[res] = ResponsibleEvent.objects.get(event=event, user=res).done

            can_resolve = context['can_all']
            if context['is_responsible'] and context['can_all']:
                can_resolve = can_resolve and ResponsibleEvent.objects.get(event=event, user=user).done

            context['can_resolve'] = can_resolve
            context['gp_table'] = gp_table
            context['responsible'] = responsible
            context['conflict_users'] = conflict_users
            context['not_main_users'] = not_main_users
        return context

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user
        checks = global_checks(user, event)
        tasks_ok = (event.tasks.exclude(status="closed").count() == 0)
        assignees = get_event_assignees(event)

        can_resolve = checks['can_all']
        if checks['is_responsible'] and checks['can_all']:
            can_resolve = can_resolve and ResponsibleEvent.objects.get(event=event, user=user).done

        if tasks_ok:
            if can_resolve:
                for assignee in assignees:
                    PointOperation.objects.filter(user=assignee, description="За " + event.name).delete()
                    create_point_op(request, assignee, event, user)
            elif checks['is_responsible'] and event.status == 'open':
                for assignee in assignees:
                    PointOperation.objects.filter(user=assignee, description="За " + event.name,
                                                  moderator=user).delete()
                    create_point_op(request, assignee, event, user)

                through = ResponsibleEvent.objects.get(event=event, user=user)
                through.done = True
                through.save()
            else:
                raise PermissionDenied

            if event.status == 'open':
                checks = check_event_closing(event)
                if checks['all_ok'] or (can_resolve and checks['only_main_gp'] and not checks['has_conflicts']):
                    event.status = 'closed'
                    event.save()
            return HttpResponseRedirect(reverse('activism:event', kwargs={'pk': event.pk}))
        else:
            raise PermissionDenied

# EventClosingView  - end


class EventBestView(GroupRequiredMixin, LoginRequiredMixin, DefaultContextMixin, DetailView):
    model = Event
    group_required = 'Ответственные за активистов'
    template_name = "activism/event_best.html"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(EventBestView, self).get_context_data(**kwargs)
        event = self.get_object()
        assignees = get_event_assignees(event)
        context['assignees'] = assignees

        star_table = OrderedDict()
        for assignee in assignees:
            op = PointOperation.objects.filter(user=assignee, description="Лучший активист " + event.name)
            if op.count() == 1:
                star_table[assignee] = list(op)[0]
            elif op.count() == 0:
                star_table[assignee] = False
        context['star_table'] = star_table

        return context

    def get(self, request, *args, **kwargs):
        if self.get_object().status == 'closed':
            return super(EventBestView, self).get(request, args, kwargs)
        else:
            raise PermissionDenied


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, JsonCreateMixin, JsonErrorsMixin, CreateView):
    model = Task
    template_name = 'activism/task_create.html'
    form_class = TaskCreateForm
    raise_exception = True

    def test_func(self, user):
        checks = global_checks(user)
        return checks['can_create_tasks']

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# TaskActionView - begin

def table_actions(request, task, action):
    if action == 'resolved':
        for key in request.POST.keys():
            if key.split('_')[0] == 'hours':
                user_hours = request.POST[key]
                through = task.participants.get(user__pk=key.split('_')[1])
                through.done = True
                through.hours = user_hours
                through.save()
    elif action == 'close':
        table_actions(request, task, 'resolved')
        task.datetime_closed = timezone.now()
        for u in task.assignees.all():
            through = task.participants.get(user=u)
            through.approved = True
            po = PointOperation.objects.create(user=through.user,
                                        amount=through.hours / 10,
                                        timestamp=task.datetime_closed,
                                        description='За ЧРА',
                                        for_hours_of_work=True)
            po.save()
            through.level_at_completion = get_level(User.objects.get(pk=through.user.pk))['num']
            through.save()
        task.save()
    elif action == 'in_progress' or action == 'open':
        if task.candidates.count() != 0:
            task.rejected.add(*task.candidates.all())
            task.candidates.clear()
        task.save()
    elif action == 'delete':
        task.delete()
    elif action == 'do':
        task.candidates.add(request.user)
    elif action == 'prop':
        task.is_urgent = request.POST['is_urgent'] if (request.POST.get('is_urgent') is not None) else False
        task.is_hard = request.POST['is_hard'] if (request.POST.get('is_hard') is not None) else False
        task.save()


def table_post(request, task, action):
    if action == 'resolved':
        return task.participants.filter(done=True).count() == task.participants.all().count()
    elif action == 'delete':
        return False
    elif action == 'prop':
        return False
    elif action == 'do':
        return False
    else:
        return True


class TaskActionView(LoginRequiredMixin, GroupRequiredMixin, SingleObjectMixin, View):
    model = Task
    group_required = "Активисты"
    raise_exception = True

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        action = kwargs['action']
        user = request.user
        checks = global_checks(user, task)

        # Preconditions
        task_number_ok = (task.assignees.all().count() >= task.number_of_assignees)
        can_all = checks['can_all']
        can_manage = checks['can_manage']
        can_close = can_manage and (checks['is_main'] or can_all)
        can_resolve = (not can_close) and (checks['is_assignee'] or checks['is_responsible'])
        can_do = (user not in task.candidates.all() and
                  user not in task.assignees.all() and
                  user not in task.rejected.all())

        # Route table
        table = {'in_labor':     {'open':        ('in_labor',    can_manage)},
                 'in_progress':  {'in_labor':    ('in_progress', can_manage and task_number_ok),
                                  'open':        ('in_progress', can_manage and task_number_ok)},
                 'resolved':     {'in_progress': ('resolved',    can_resolve)},
                 'not_resolved': {'resolved':    ('in_progress', can_manage)},
                 'close':        {'resolved':    ('closed',      can_close),
                                  'in_progress': ('closed',      can_manage),
                                  'closed':      ('closed',      can_close)},
                 'open':         {'in_labor':    ('open',        can_manage)},
                 'delete':       {'open':        (None,          can_manage),
                                  'in_labor':    (None,          can_manage),
                                  'in_progress': (None,          can_all)},
                 'do':           {'in_labor':    (None,          can_do)},
                 'prop':         {'any':         (None,          can_all)}}

        # Transition
        if table.get(action) is not None:
            init = table[action]

            status = 'any' if (init.get('any') is not None) else task.status
            if init.get(status) is not None:
                if init[status][1]:
                    table_actions(request, task, action)
                    if table_post(request, task, action):
                        task.status = init[status][0]
                        task.save()
                    if task.pk is not None:
                        return JsonResponse({'url': reverse('activism:task', kwargs={'pk': task.pk})}, status=200)
                    else:
                        return JsonResponse({'url': reverse('activism:index')}, status=200)
                else:
                    raise PermissionDenied
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

# TaskActionView - end


class AddPointsView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = User
    form_class = PointForm
    group_required = 'Ответственные за активистов'
    raise_exception = True
    context_object_name = 'user'
    template_name = 'activism/add_points.html'

    def form_invalid(self, form):
        super(AddPointsView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        PointOperation.objects.create(user=self.get_object(),
                                      amount=form.cleaned_data['amount'],
                                      timestamp=timezone.now(),
                                      description=form.cleaned_data['description'],
                                      moderator=self.request.user)
        return JsonResponse({'url': reverse('activism:activists')}, status=200)


class DeletePointsView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = PointOperation
    group_required = 'Ответственные за активистов'
    success_url = reverse_lazy('activism:activists')
    raise_exception = True


class TaskCommentCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """
    Действие создания комментария
    """
    model = TaskComment
    group_required = 'Активисты'
    form_class = TaskCommentForm
    raise_exception = True

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.task = Task.objects.get(pk=self.kwargs['task_pk'])
        return super(TaskCommentCreateView, self).form_valid(form)


class TaskCommentUpdateView(LoginRequiredMixin, GroupRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Действие редактирования комментария
    """
    model = TaskComment
    group_required = 'Активисты'
    form_class = TaskCommentForm
    raise_exception = True

    def test_func(self, user):
        return self.get_object().user == user


class TaskCommentDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    """
    Действие удаления комментария
    """
    model = TaskComment
    group_required = 'Ответственные за активистов'
    success_url = reverse_lazy('activism:activists')
    raise_exception = True

"""
    Show views
"""


class IndexView(LoginRequiredMixin, DefaultContextMixin, TemplateView):
    template_name = 'activism/dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(IndexView, self).get_context_data(**kwargs)
        context['labor'] = chain(Task.objects.filter(is_urgent=True, status='in_labor').order_by('datetime_limit'),
                                 Task.objects.filter(is_urgent=False, status='in_labor').order_by('datetime_limit'))
        context['events'] = context['events'].filter(status='open',
                                                     date_held__gte=timezone.now().date()).order_by('date_held')[:5]
        context['bids'] = \
            sorted(chain(user.tasks_approve.all(),
                         user.task_set.filter(status__in=['open', 'in_labor']),
                         user.tasks_rejected.exclude(status='closed')),
                   key=lambda instance: instance.datetime_limit)
        context['tasks_current'] = user.task_set.filter(status__in=['in_progress', 'resolved']).order_by('datetime_limit')
        context['tasks_responsible'] = user.tasks_responsible.exclude(status='closed')
        return context


class EventsView(LoginRequiredMixin, GroupRequiredMixin, DefaultContextMixin, ListView):
    model = Event
    template_name = 'activism/events.html'
    context_object_name = 'events'
    group_required = "Активисты"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        context['events'] = sorted(context['events'].filter(status__in=['open']),
                                   key=lambda event: event.date_held - timezone.now().date())
        return context


class EventView(LoginRequiredMixin, GroupRequiredMixin, PostAccessMixin, DefaultContextMixin, JsonErrorsMixin, UpdateView):
    model = Event
    template_name = 'activism/event.html'
    form_class = EventForm
    group_required = "Активисты"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user
        tasks_ok = (event.tasks.all().exclude(status="closed").count() == 0)
        context['can_close'] = (context['is_responsible'] or context['can_all']) and event.status == 'open' and tasks_ok
        context['can_edit'] = (context['is_responsible'] or context['can_all']) and event.status == 'open'
        context['can_add_responsible'] = (context['is_main'] or context['can_all']) and event.status == 'open'
        context['operations'] = PointOperation.objects.filter(description="За "+event.name)
        return context


class TaskView(LoginRequiredMixin, GroupRequiredMixin, PostAccessMixin, DefaultContextMixin, JsonErrorsMixin, UpdateView):
    model = Task
    template_name = 'activism/task.html'
    form_class = TaskForm
    group_required = "Активисты"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        user = self.request.user
        task = context['task']
        if not context['is_main'] and not context['can_all']:
            context['events'] = Event.objects.filter(pk__in=user.event_responsible
                                                                .filter(event__status='open')
                                                                .values_list('event', flat=True))
        context['can_edit'] = context['can_manage'] and task.status != 'closed'
        context['can_close'] = ((context['can_manage']) and (context['is_main'] or context['can_all']) and
                                (task.status == 'resolved' or task.status == 'in_progress')) or \
                               (task.status == 'closed' and context['can_all'])
        context['can_resolve'] = (not context['can_close']) and task.status == 'in_progress' and \
                                 (context['can_manage'] or user in task.assignees.all())
        context['is_blocked'] = not (task.status == 'open' or task.status == 'in_labor')
        context['can_edit_sector'] = context['can_edit'] and (context['is_main'] or context['can_all'])
        context['can_edit_event'] = (context['can_edit'] and not context['is_blocked'])
        context['can_resign_assignee'] = (context['can_edit'] and not context['is_blocked']) or context['can_all']
        context['through'] = task.participants.all()
        return context

    def form_valid(self, form):
        task = self.get_object()
        user = self.request.user
        checks = global_checks(user, task)
        if hasattr(form.cleaned_data, 'event'):
            if not (checks['can_choose_all_events']):
                if form.cleaned_data['event'] not in Event.objects.filter(pk__in=user.event_responsible
                                                                                     .filter(event__status='open')
                                                                                     .values_list('event', flat=True)):
                    return super(TaskView, self).form_invalid(form)
        result = super(TaskView, self).form_valid(form)
        for u in list(set(task.assignees.all()).union(set(task.candidates.all())).union(set(task.rejected.all()))):
            if u in task.assignees.all() and u in task.candidates.all():
                task.candidates.remove(u)
            if u in task.assignees.all() and u in task.rejected.all():
                task.rejected.remove(u)
        return result


class SectorView(LoginRequiredMixin, DetailView):
    model = Sector
    template_name = "activism/sector.html"


class ActivistsView(LoginRequiredMixin, GroupRequiredMixin, DefaultContextMixin, TemplateView):
    template_name = 'activism/activists.html'
    group_required = "Активисты"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(ActivistsView, self).get_context_data(**kwargs)
        activists = sorted(Group.objects.get(name='Активисты').user_set.all(),
                           key=lambda u: u.last_name)

        records = []
        show_all = global_checks(self.request.user)['can_all']
        for user in activists:
            if Group.objects.get(name="Руководящая группа") not in user.groups.all() and \
               Group.objects.get(name="Ответственные за активистов") not in user.groups.all():
                level = get_level(user)
                if show_all:
                    throughs = user.participated.filter(task__status__in=['closed'])
                    sum_hours = sum(throughs.values_list('hours', flat=True))
                    operations = user.pointoperations.filter(for_hours_of_work=False)
                    sum_og = sum(user.pointoperations.filter(for_hours_of_work=False).values_list('amount', flat=True))
                    sum_all = sum_og + int(sum_hours // 10)
                    records.append({'user': user,
                                    'throughs': throughs,
                                    'sum_hours': sum_hours,
                                    'operations': operations,
                                    'sum_og': sum_og,
                                    'sum_all': sum_all,
                                    'level': level['sign']})
                else:
                    records.append({'user': user,
                                    'sum_all': math.floor(user.profile.experience),
                                    'level': level['sign']})

        context['records'] = list(sorted(records, key=lambda record: (-record['sum_all'], record['user'].last_name)))
        context['records'] = list(sorted(records, key=lambda record: (-record['sum_all'], record['user'].last_name)))
        return context


class RatingView(LoginRequiredMixin, GroupRequiredMixin, DefaultContextMixin, TemplateView):
    template_name = 'activism/rating.html'
    group_required = "Активисты"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(RatingView, self).get_context_data(**kwargs)
        activists = sorted(Group.objects.get(name='Активисты').user_set.all(),
                           key=lambda u: u.last_name)
        records = {}
        dates = []
        context['records'] = OrderedDict()
        current_date = (timezone.now().year, timezone.now().month)
        for i in range(6):
            month = current_date[1] - i
            year = current_date[0]
            if month < 1:
                month += 12
                year -= 1
            dates.append((year, month))
        for date in dates:
            date_str = dt.datetime(year=date[0], month=date[1], day=1)
            records[date_str] = []
            for user in activists:
                if Group.objects.get(name="Руководящая группа") not in user.groups.all() and \
                   Group.objects.get(name="Ответственные за активистов") not in user.groups.all():
                    throughs = user.participated.filter(task__status__in=['closed'],
                                                        task__datetime_closed__year=date[0],
                                                        task__datetime_closed__month=date[1])
                    sum_hours = sum(throughs.values_list('hours', flat=True))
                    if sum_hours != 0:
                        records[date_str].append({'user': user,
                                                  'sum_hours': sum_hours})

            context['records'][date_str] = list(
                reversed(sorted(
                    reversed(sorted(records[date_str],
                             key=lambda record: record['user'].last_name)),
                         key=lambda record: record['sum_hours'])))
        return context


# TaskLog - begin

def dict_diff(first, second):
    diff = {}
    for key in first.keys():
        if first[key] != second[key]:
            diff[key] = (first[key], second[key])
    return diff


def get_full_names(pks):
    return [user.get_full_name() for user in User.objects.filter(pk__in=pks)]


def get_through_pks(version):
    return [through.field_dict['user'] for through in version.revision.version_set.all().filter(content_type=27)]


class TaskLogView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = Task
    template_name = 'activism/task_log.html'
    group_required = "Активисты"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(TaskLogView, self).get_context_data(**kwargs)
        version_list = get_for_object(self.get_object())
        records = []
        for index in range(len(version_list)):
            actions = []
            version = version_list[index]
            if index == len(version_list) - 1:
                actions.append({'name': 'Начальное состояние', 'flag': True})
            else:
                prev_version = version_list[index + 1]
                diff = dict_diff(prev_version.field_dict, version.field_dict)
                for key in diff.keys():
                    if key not in ['datetime_last_modified', ]:
                        name = str(Task._meta.get_field(key).verbose_name)
                        if key in ['candidates', 'responsible', 'rejected']:
                            old = ', '.join(get_full_names(diff[key][0]))
                            new = ', '.join(get_full_names(diff[key][1]))
                        else:
                            old = str(diff[key][0])
                            new = str(diff[key][1])
                        actions.append({'name': name, 'old': old, 'new': new})
                if len(prev_version.revision.version_set.all()) != len(version.revision.version_set.all()):
                    name = "Исполнители"
                    old = ', '.join(get_full_names(get_through_pks(prev_version)))
                    new = ', '.join(get_full_names(get_through_pks(version)))
                    actions.append({'name': name, 'old': old, 'new': new})

            records.append({'user': version.revision.user,
                            'date': version.field_dict['datetime_last_modified'],
                            'actions': actions})
        context['records'] = records
        return context

# TaskLog - end

def get_valid_activists():
    users = Group.objects.get(name='Активисты').user_set.all()
    activists = []
    for user in users:
        if Group.objects.get(name="Руководящая группа") not in user.groups.all() and \
                        Group.objects.get(name="Ответственные за активистов") not in user.groups.all() and \
                        get_level(user)['num'] != 0:
            activists.append(user)
    activists.sort(key=lambda u: u.last_name)
    return activists

def get_affected_tasks(user, begin, end):
    user_tasks = user.participated.filter(task__status__in=['closed']).order_by('task__datetime_closed')
    time = None
    if get_level(user)['num'] > 0:
        for task in user_tasks:
            if task.level_at_completion > 0:
                time = task.task.datetime_closed
                break
    if not time or time < begin or time > end:
        user_tasks = user_tasks.filter(task__datetime_closed__gte=begin, task__datetime_closed__lte=end, rewarded=False)
    else:
        user_tasks = user_tasks.filter(task__datetime_closed__lte=end, rewarded=False)
    return user_tasks

def generate_payments_table_context(valuedict):
    const = float(valuedict['const']) if 'const' in valuedict else 2000

    begin = dt.datetime.combine(timezone.now().date(), dt.time(0)) - dt.timedelta(days=30)
    if 'begin' in valuedict:
        begin = dt.datetime.strptime(valuedict['begin'], '%Y-%m-%d')

    end = dt.datetime.combine(timezone.now().date(), dt.time(0))
    if 'end' in valuedict:
        end = dt.datetime.strptime(valuedict['end'], '%Y-%m-%d')

    context = dict()
    context['const'] = const
    context['begin'] = begin
    context['end'] = end

    records = []
    users = get_valid_activists()
    for user in users:
        pure_hours = user.participated.filter(task__status__in=['closed'],
                                              task__datetime_closed__gte=begin,
                                              task__datetime_closed__lte=end).aggregate(Sum('hours'))['hours__sum']
        if not pure_hours:
            pure_hours = 0
        if pure_hours > 0 or user.profile.payments > 0:
            user_tasks = get_affected_tasks(user, begin, end)
            records.append({'user': user,
                            'effective_hours': sum(
                                task.hours * get_level_by_num(task.level_at_completion)['coef'] for task in user_tasks),
                            'hours': pure_hours,
                            'holded_payment': user.profile.payments})
    for record in records:
        record['payment'] = const * record['effective_hours']
    context['payment_sum'] = sum(record['payment'] for record in records)
    context['holded_payment_sum'] = sum(record['holded_payment'] for record in records)
    context['records'] = sorted(records, key=lambda record: record['payment'], reverse=True)
    return context

class PaymentsView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = "Ответственные за активистов"
    template_name = 'activism/payments.html'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        users = get_valid_activists()
        if not {'const', 'begin', 'end'}.issubset(request.POST):
            return JsonResponse(status=400)
        const = float(request.POST['const'])
        begin = dt.datetime.strptime(request.POST['begin'], '%Y-%m-%d')
        end = dt.datetime.strptime(request.POST['end'], '%Y-%m-%d')
        for user in users:
            tasks = get_affected_tasks(user, begin, end)
            if len(tasks) > 0:
                total = 0
                for task in tasks:
                    task.rewarded = True
                    total += task.hours * get_level_by_num(task.level_at_completion)['coef']
                    task.save()
                total *= const
                po = PaymentsOperation.objects.create(user=user, amount = round(total), timestamp = timezone.now(),
                                                 description="За ЧРА " + timezone.now().ctime())
                po.save()
        return JsonResponse({'action' : 'refresh'}, status=200)

    def get_context_data(self, **kwargs):
        context = super(PaymentsView, self).get_context_data(**kwargs)
        context.update(generate_payments_table_context(self.request.GET))
        return context

class ExportPaymentsTableView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = "Ответственные за активистов"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        context = generate_payments_table_context(request.GET)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="table_'+\
            context['begin'].strftime("%Y-%m-%d") + '_' +\
            context['end'].strftime("%Y-%m-%d") + '.csv"'
        writer = csv.writer(response)
        writer.writerow(['Константа', 'Начало', 'Конец'])
        writer.writerow([context['const'], context['begin'], context['end']])
        writer.writerow(['Активист',
                        'Группа',
                        'Часы',
                        'Невыплаченно ранее',
                        'Деньги за период',
                        'Эффективные часы'])
        for record in context['records']:
            l = []
            l.append(record['user'].last_name + ' ' + record['user'].first_name + ' ' + record['user'].profile.middle_name)
            l.append(record['user'].profile.group_number)
            l.append(record['hours'])
            l.append(record['effective_hours'])
            l.append(record['holded_payment'])
            l.append(record['payment'])
            writer.writerow(l)
        return response