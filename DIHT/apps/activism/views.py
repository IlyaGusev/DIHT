import logging
from itertools import chain
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, View, CreateView, TemplateView, DetailView, DeleteView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from braces.views import LoginRequiredMixin, GroupRequiredMixin, UserPassesTestMixin
from reversion import get_for_object
from activism.models import Event, Task, AssigneeTask, Sector, PointOperation
from activism.forms import TaskForm, EventForm, TaskCreateForm, PointForm

logger = logging.getLogger('DIHT.custom')


def get_level(user):
    if Group.objects.get(name="Руководящая группа") in user.groups.all():
        return 4

    hours = sum(user.participated.filter(task__status__in=['closed']).values_list('hours', flat=True))
    gp = hours // 10 + sum(user.point_operations.all().values_list('amount', flat=True))

    if gp < 4:
        return {'sign': 'Активист-новичок', 'coef': 0}
    elif gp < 16:
        return {'sign': 'Активист', 'coef': 1}
    elif gp < 35:
        return {'sign': 'Активист-организатор', 'coef': 1.7}
    elif gp < 70:
        return {'sign': 'Активист-лидер', 'coef': 2.4}
    else:
        return {'sign': 'Активист-руководитель', 'coef': 4}

"""
    Mixins
"""


class PostAccessMixin(SingleObjectMixin):
    def post(self, request, *args, **kwargs):
        if request.user in self.get_object().responsible.all() or request.user.is_superuser or \
                (Group.objects.get(name="Ответственные за активистов") in request.user.groups.all()) or \
                (Group.objects.get(name="Руководящая группа") in request.user.groups.all()):
                return super(PostAccessMixin, self).post(request, args, kwargs)
        else:
            raise PermissionDenied


class DefaultContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(DefaultContextMixin, self).get_context_data(**kwargs)
        user = self.request.user
        context['is_superuser'] = user.is_superuser
        context['is_charge'] = Group.objects.get(name="Ответственные за активистов") in user.groups.all()
        context['is_main'] = Group.objects.get(name="Руководящая группа") in user.groups.all()
        context['can_all'] = context['is_charge'] or context['is_superuser']
        context['events'] = Event.objects.all()
        context['sectors'] = Sector.objects.all()
        context['users'] = User.objects.all()
        context['can_manage'] = context['is_charge'] or context['is_superuser']
        if hasattr(self, 'object'):
            obj = self.get_object()
            context['is_responsible'] = (user in obj.responsible.all())
            context['can_manage'] = context['can_manage'] or context['is_responsible']
            if hasattr(obj, 'sector'):
                if obj.sector is not None:
                    context['can_manage'] = context['can_manage'] or obj.sector.main == user
        return context


class JsonCreateMixin(object):
    def form_valid(self, form):
        result = super(JsonCreateMixin, self).form_valid(form)
        form.instance.responsible.add(self.request.user)
        return JsonResponse({'url': result.url}, status=200)


class JsonErrorsMixin(object):
    def form_invalid(self, form):
        super(JsonErrorsMixin, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


"""
    Action views
"""


class UnlockView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, *args, **kwargs):
        user = request.user
        user.groups.add(Group.objects.get(name="Активисты"))
        return HttpResponseRedirect(reverse('activism:index'))


class EventCreateView(LoginRequiredMixin, GroupRequiredMixin, JsonCreateMixin, JsonErrorsMixin, CreateView):
    model = Event
    template_name = 'activism/event_create.html'
    fields = ('name', 'sector')
    group_required = ["Руководящая группа", "Ответственные за активистов"]
    raise_exception = True


class EventActionView(SingleObjectMixin, GroupRequiredMixin, LoginRequiredMixin, View):
    model = Event
    group_required = "Активисты"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        action = kwargs['action']
        user = request.user
        is_responsible = (user in event.responsible.all())
        is_charge = (Group.objects.get(name="Ответственные за активистов") in request.user.groups.all())
        can_all = user.is_superuser or is_charge
        tasks_ok = (event.tasks.exclude(status="closed").count() == 0)

        if ((is_responsible and tasks_ok) or can_all) and action == "close" and event.status == 'open':
            event.status = 'closed'
            event.save()
            return HttpResponseRedirect(reverse('activism:index'))
        else:
            raise PermissionDenied


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, JsonCreateMixin, JsonErrorsMixin, CreateView):
    model = Task
    template_name = 'activism/task_create.html'
    form_class = TaskCreateForm
    raise_exception = True

    def test_func(self, user):
        is_charge = Group.objects.get(name="Ответственные за активистов") in user.groups.all()
        is_main = Group.objects.get(name="Руководящая группа") in user.groups.all()
        return user.events.count() != 0 or is_main or user.is_superuser or is_charge

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskActionView(LoginRequiredMixin, GroupRequiredMixin, SingleObjectMixin, View):
    model = Task
    group_required = "Активисты"
    raise_exception = True

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        action = kwargs['action']
        user = request.user
        is_charge = (Group.objects.get(name="Ответственные за активистов") in user.groups.all())
        is_main = Group.objects.get(name="Руководящая группа") in user.groups.all()
        is_responsible = user in task.responsible.all()
        is_assignee = (user in task.assignees.all())
        is_sector_main = False
        if task.sector is not None:
            is_sector_main = (task.sector.main == user)
        task_number_ok = (task.assignees.all().count() >= task.number_of_assignees)
        task_status_ok = task.status == 'in_labor' or task.status == 'open'
        can_all = user.is_superuser or is_charge
        can_manage = is_responsible or can_all or is_sector_main
        can_close = can_manage and (is_main or can_all)
        can_resolve = (not can_close) and (can_manage or is_assignee)

        table = {'in_labor': {'open': ('in_labor', can_manage)},
                 'in_progress': {'in_labor': ('in_progress', can_manage and task_number_ok),
                                 'open': ('in_progress', can_manage and task_number_ok)},
                 'resolved': {'in_progress': ('resolved', can_resolve)},
                 'not_resolved': {'resolved': ('in_progress', can_manage)},
                 'close': {'resolved': ('closed', can_close),
                           'in_progress': ('closed', can_manage),
                           'closed': ('closed', can_close)},
                 'open': {'in_labor': ('open', can_manage)}}

        if action == 'prop':
            if can_all:
                if request.POST.get('is_urgent') is not None:
                    task.is_urgent = request.POST['is_urgent']
                else:
                    task.is_urgent = False
                if request.POST.get('is_hard') is not None:
                    task.is_hard = request.POST['is_hard']
                else:
                    task.is_hard = False
                task.save()
                return JsonResponse({'url': reverse('activism:task', kwargs={'pk': task.pk})}, status=200)
            else:
                raise PermissionDenied

        if action == 'do':
            if user not in task.candidates.all() and \
               user not in task.assignees.all() and \
               user not in task.rejected.all():
                task.candidates.add(request.user)
                task.save()
                return JsonResponse({'url': reverse('activism:index')}, status=200)
            else:
                raise PermissionDenied

        if action == 'delete':
            if (is_responsible and task_status_ok) or can_all:
                task.delete()
                return JsonResponse({'url': reverse('activism:index')}, status=200)
            else:
                raise PermissionDenied

        if table.get(action) is not None:
            init = table[action]
            if init.get(task.status) is not None:
                if init[task.status][1]:
                    if action == 'resolved' or action == 'close':
                        for user in task.assignees.all():
                            user_hours = request.POST['hours_' + str(user.pk)]
                            through = task.participants.get(user=user)
                            through.hours = user_hours
                            if action == 'close':
                                through.approved = True
                                task.datetime_closed = timezone.now()
                            through.save()
                    task.status = init[task.status][0]
                    task.save()
                    if task.status != 'in_labor':
                        if task.candidates.count() != 0:
                            task.rejected.add(*task.candidates.all())

                            task.candidates.clear()
                    return JsonResponse({'url': reverse('activism:task', kwargs={'pk': task.pk})}, status=200)
                else:
                    raise PermissionDenied
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied


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
            context['events'] = user.events.filter(status='open')
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
        is_charge = (Group.objects.get(name="Ответственные за активистов") in user.groups.all())
        is_main = Group.objects.get(name="Руководящая группа") in user.groups.all()
        if hasattr(form.cleaned_data, 'event'):
            if not is_main and not user.is_superuser and not is_charge:
                if form.cleaned_data['event'] not in user.events.all():
                    return super(TaskView, self).form_invalid(form)
        result = super(TaskView, self).form_valid(form)
        if user in task.assignees.all() and user in task.candidates.all():
            task.candidates.remove(user)
        if user in task.assignees.all() and user in task.rejected.all():
            task.rejected.remove(user)
        return result


class SectorView(LoginRequiredMixin, DetailView):
    model = Sector
    template_name = "activism/sector.html"


class ActivistsView(LoginRequiredMixin, GroupRequiredMixin, DefaultContextMixin, ListView):
    model = User
    template_name = 'activism/activists.html'
    group_required = "Активисты"
    context_object_name = 'users'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(ActivistsView, self).get_context_data(**kwargs)
        activists = sorted([user for user in Group.objects.get(name='Активисты').user_set.all()], key=lambda user: user.last_name)

        records = []
        for user in activists:
            if Group.objects.get(name="Руководящая группа") not in user.groups.all() and \
               Group.objects.get(name="Ответственные за активистов") not in user.groups.all():
                throughs = user.participated.filter(task__status__in=['closed'])
                sum_hours = sum(throughs.values_list('hours', flat=True))
                operations = user.point_operations.all()
                sum_og = sum(user.point_operations.all().values_list('amount', flat=True))
                sum_all = sum_og + int(sum_hours // 10)
                level = get_level(user)
                records.append({'user': user,
                                'throughs': throughs,
                                'sum_hours': sum_hours,
                                'operations': operations,
                                'sum_og': sum_og,
                                'sum_all': sum_all,
                                'level': level['sign']})
        context['records'] = list(reversed(sorted(sorted(reversed(sorted(records, key=lambda record: record['user'].last_name)),
                                                         key=lambda record: record['sum_hours']),
                                                  key=lambda record: record['sum_all'])))
        return context


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
                        if key in ['candidates', 'responsible']:
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