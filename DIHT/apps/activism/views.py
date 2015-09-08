import logging
from itertools import chain
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, View, CreateView, TemplateView, DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from braces.views import LoginRequiredMixin, GroupRequiredMixin, UserPassesTestMixin
from activism.models import Event, Task, AssigneeTask, Sector
from activism.forms import TaskForm, EventForm, TaskCreateForm

logger = logging.getLogger('DIHT.custom')

"""
    Mixins
"""


class CreatorMixin(SingleObjectMixin):
    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().creator or request.user.is_superuser or \
                (Group.objects.get(name="Ответственные за волонтёров") in request.user.groups.all()):
                return super(CreatorMixin, self).post(request, args, kwargs)
        else:
            raise PermissionDenied


class DefaultContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(DefaultContextMixin, self).get_context_data(**kwargs)
        user = self.request.user
        context['is_superuser'] = user.is_superuser
        context['is_charge'] = Group.objects.get(name="Ответственные за волонтёров") in user.groups.all()
        context['is_main'] = Group.objects.get(name="Руководящая группа") in user.groups.all()
        context['can_all'] = context['is_charge'] or context['is_superuser']
        context['events'] = Event.objects.all()
        context['sectors'] = Sector.objects.all()
        context['users'] = User.objects.all()
        context['can_manage'] = context['is_charge'] or context['is_superuser']
        if hasattr(self, 'object'):
            obj = self.get_object()
            context['is_creator'] = (user == obj.creator)
            context['can_manage'] = context['can_manage'] or context['is_creator']
        return context


class JsonCreateMixin(object):
    def form_valid(self, form):
        form.instance.creator = self.request.user
        result = super(JsonCreateMixin, self).form_valid(form)
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
    group_required = ["Руководящая группа", "Ответственные за волонтёров"]
    raise_exception = True


class EventActionView(SingleObjectMixin, GroupRequiredMixin, LoginRequiredMixin, View):
    model = Event
    group_required = "Активисты"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        action = kwargs['action']
        user = request.user
        is_creator = (user == event.creator)
        is_charge = (Group.objects.get(name="Ответственные за волонтёров") in request.user.groups.all())
        can_all = user.is_superuser or is_charge
        tasks_ok = (event.tasks.exclude(status="closed").count() == 0)

        if ((is_creator and tasks_ok) or can_all) and action == "close" and event.status == 'open':
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
        is_charge = Group.objects.get(name="Ответственные за волонтёров") in user.groups.all()
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
        is_charge = (Group.objects.get(name="Ответственные за волонтёров") in user.groups.all())
        is_creator = user == task.creator
        is_assignee = (user in task.assignees.all())
        task_number_ok = (task.assignees.all().count() >= task.number_of_assignees)
        task_status_ok = task.status == 'in_labor' or task.status == 'open'
        can_all = user.is_superuser or is_charge
        can_manage = is_creator or can_all

        table = {'in_labor': {'open': ('in_labor', can_manage)},
                 'in_progress': {'in_labor': ('in_progress', can_manage and task_number_ok),
                                 'open': ('in_progress', can_manage and task_number_ok)},
                 'resolved': {'in_progress': ('resolved', is_assignee)},
                 'not_resolved': {'resolved': ('in_progress', can_manage)},
                 'close': {'resolved': ('closed', can_manage),
                           'in_progress': ('closed', can_manage)},
                 'open': {'in_labor': ('open', can_manage)}}

        if action == 'prop':
            if (is_creator and task_status_ok) or can_all:
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
            if (is_creator and task_status_ok) or can_all:
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
                            user_hours = request.POST['hours_'+str(user.pk)]
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


"""
    Show views
"""


class IndexView(LoginRequiredMixin, DefaultContextMixin, TemplateView):
    template_name = 'activism/dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(IndexView, self).get_context_data(**kwargs)
        context['labor'] = Task.objects.filter(status__in=['in_labor'])
        context['events'] = context['events'].filter(status='open').order_by('date_held')[:5]
        context['bids'] = \
            sorted(chain(user.tasks_approve.all(),
                         user.task_set.filter(status__in=['open', 'in_labor']),
                         user.tasks_rejected.exclude(status='closed')),
                   key=lambda instance: instance.datetime_limit)
        context['tasks_current'] = user.task_set.filter(status__in=['in_progress', 'resolved']).order_by('datetime_limit')
        context['tasks_created'] = user.tasks_created.exclude(status='closed')
        return context


class EventsView(LoginRequiredMixin, GroupRequiredMixin, DefaultContextMixin, ListView):
    model = Event
    template_name = 'activism/events.html'
    context_object_name = 'events'
    group_required = "Активисты"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        context['events'] = context['events'].filter(status__in=['open'])
        return context


class EventView(LoginRequiredMixin,  GroupRequiredMixin, CreatorMixin, DefaultContextMixin, JsonErrorsMixin, UpdateView):
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
        context['can_close'] = ((context['is_creator'] and tasks_ok) or context['can_all']) and event.status == 'open'
        context['can_edit'] = ((context['is_creator'] and event.status == 'open') or context['can_all'])
        context['can_create_tasks'] = user in event.assignees.all()
        return context


class TaskView(LoginRequiredMixin, GroupRequiredMixin, CreatorMixin, DefaultContextMixin, JsonErrorsMixin, UpdateView):
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
        context['can_edit'] = (context['is_creator'] and (task.status == 'open' or task.status == 'in_labor')) or context['can_all']
        context['can_edit_always'] = (context['is_creator'] and task.status != 'closed') or context['can_all']
        context['through'] = task.participants.all()
        return context

    def form_valid(self, form):
        task = self.get_object()
        user = self.request.user
        is_charge = (Group.objects.get(name="Ответственные за волонтёров") in user.groups.all())
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


class ClosedTasksView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Task
    template_name = 'activism/closed.html'
    group_required = "Ответственные за волонтёров"
    raise_exception = True
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super(ClosedTasksView, self).get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(status__in=['closed']).order_by('-datetime_last_modified')
        return context


class ActivistsView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = User
    template_name = 'activism/activists.html'
    group_required = "Активисты"
    raise_exception = True
    context_object_name = 'users'
    
    def get_context_data(self, **kwargs):
        context = super(ActivistsView, self).get_context_data(**kwargs)
        print (context['users'])
        activists = [user for user in list(context['users'].all()) if Group.objects.get(name='Активисты') in user.groups.all()]
        context['users'] = sorted(activists, key=lambda user: user.last_name)
        return context