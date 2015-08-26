import logging
from itertools import chain
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, View, CreateView, TemplateView, DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.utils import timezone
from braces.views import LoginRequiredMixin, GroupRequiredMixin, UserPassesTestMixin
from activism.models import Event, Task, AssigneeTask, Sector
from activism.forms import TaskForm, EventForm, TaskCreateForm

logger = logging.getLogger('DIHT.custom')


class CreatorMixin(SingleObjectMixin):
    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super(CreatorMixin, self).post(request, args, kwargs)
        else:
            raise PermissionDenied


class UnlockView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, *args, **kwargs):
        user = request.user
        user.groups.add(Group.objects.get(name="Активисты"))
        return HttpResponseRedirect(reverse('activism:index'))


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'activism/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['labor'] = Task.objects.filter(status__in=['in_labor'])
        context['events'] = Event.objects.filter(status='open').order_by('date_held')[:5]
        user = self.request.user
        context['bids'] = \
            sorted(chain(user.tasks_approve.all(),
                         user.task_set.filter(status__in=['open', 'in_labor']),
                         user.tasks_rejected.exclude(status='closed')),
                   key=lambda instance: instance.datetime_limit)
        context['tasks_current'] = user.task_set.filter(status__in=['in_progress', 'resolved']).order_by('datetime_limit')
        context['tasks_created'] = user.tasks_created.exclude(status='closed')
        return context


class EventsView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Event
    template_name = 'activism/events.html'
    context_object_name = 'events'
    group_required = "Активисты"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        context['events'] = context['events'].filter(status__in=['open'])
        return context


class EventCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Event
    template_name = 'activism/event_create.html'
    fields = ('name', 'sector')
    group_required = "Руководящая группа"
    raise_exception = True

    def form_valid(self, form):
        form.instance.creator = self.request.user
        result = super(EventCreateView, self).form_valid(form)
        return JsonResponse({'url': result.url}, status=200)

    def form_invalid(self, form):
        super(EventCreateView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


class EventView(LoginRequiredMixin,  GroupRequiredMixin, CreatorMixin, UpdateView):
    model = Event
    template_name = 'activism/event.html'
    form_class = EventForm
    group_required = "Активисты"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user
        is_creator = (user == event.creator)
        can_close = (event.tasks.all().exclude(status="closed").count() == 0)
        context['users'] = User.objects.all()
        context['can_close'] = (is_creator and can_close and event.status == 'open')
        context['sectors'] = Sector.objects.all()
        return context

    def form_invalid(self, form):
        super(EventView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


class EventActionView(SingleObjectMixin, GroupRequiredMixin, LoginRequiredMixin, View):
    model = Event
    group_required = "Активисты"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        action = kwargs['action']
        user = request.user
        is_creator = (user == event.creator)
        can_close = (event.tasks.exclude(status="closed").count() == 0)
        if is_creator and can_close and action == "close" and event.status == 'open':
            event.status = 'closed'
            event.save()
            return HttpResponseRedirect(reverse('activism:index'))
        else:
            raise PermissionDenied


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    template_name = 'activism/task_create.html'
    form_class = TaskCreateForm
    raise_exception = True

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self, user):
        return user.events.count() != 0 or Group.objects.get(name="Руководящая группа") in user.groups.all()

    def form_valid(self, form):
        form.instance.creator = self.request.user
        result = super(TaskCreateView, self).form_valid(form)
        return JsonResponse({'url': result.url}, status=200)

    def form_invalid(self, form):
        super(TaskCreateView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


class TaskView(LoginRequiredMixin, GroupRequiredMixin, CreatorMixin, UpdateView):
    model = Task
    template_name = 'activism/task.html'
    form_class = TaskForm
    group_required = "Активисты"
    raise_exception = True

    def form_valid(self, form):
        task = self.get_object()
        user = self.request.user
        if Group.objects.get(name="Руководящая группа") not in user.groups.all():
            if form.cleaned_data['event'] not in user.events.all():
                return super(TaskView, self).form_invalid(form)
        result = super(TaskView, self).form_valid(form)
        if user in task.assignees.all() and user in task.candidates.all():
            task.candidates.remove(user)
        if user in task.assignees.all() and user in task.rejected.all():
            task.rejected.remove(user)
        return result

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        user = self.request.user
        if Group.objects.get(name="Руководящая группа") not in user.groups.all():
            context['events'] = user.events.all()
        else:
            context['events'] = Event.objects.all()
        context['sectors'] = Sector.objects.all()
        context['users'] = User.objects.all()
        context['can_edit'] = (user == context['task'].creator) and \
                              (context['task'].status == 'open' or context['task'].status == 'in_labor')
        context['through'] = context['task'].participants.all()
        return context

    def form_invalid(self, form):
        super(TaskView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


class TaskActionView(LoginRequiredMixin, GroupRequiredMixin, SingleObjectMixin, View):
    model = Task
    group_required = "Активисты"
    raise_exception = True

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        action = kwargs['action']
        user = request.user
        is_creator = (user == task.creator)
        is_assignee = (user in task.assignees.all())
        is_enough = (task.assignees.all().count() >= task.number_of_assignees)
        can_edit = task.status == 'in_labor' or task.status == 'open'
        table = {'in_labor': {'open': ('in_labor', is_creator)},
                 'in_progress': {'in_labor': ('in_progress', is_creator and is_enough),
                                 'open': ('in_progress', is_creator and is_enough)},
                 'resolved': {'in_progress': ('resolved', is_assignee)},
                 'not_resolved': {'resolved': ('in_progress', is_creator)},
                 'close': {'resolved': ('closed', is_creator),
                           'in_progress': ('closed', is_creator)},
                 'open': {'in_labor': ('open', is_creator)}}

        if action == 'prop':
            if is_creator and can_edit:
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
            if is_creator and can_edit:
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


class SectorView(LoginRequiredMixin, DetailView):
    model = Sector
    template_name = "activism/sector.html"