import logging
from django.views.generic import ListView, View, CreateView, TemplateView
from braces.views import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from activism.models import Event, Task
from activism.forms import TaskForm, TaskCreateForm
from itertools import chain


logger = logging.getLogger('DIHT.custom')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'activism/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['labor'] = Task.objects.filter(status__in=['in_labor'])
        context['events'] = \
            Event.objects.filter(status='open').order_by('date_held')[:5]
        user = self.request.user
        context['bids'] = \
            sorted(chain(user.tasks_approve.all(),
                         user.tasks.filter(status__in=['in_labor']),
                         user.tasks_rejected.exclude(status='closed')),
                   key=lambda instance: instance.datetime_limit)
        context['tasks_current'] = user.tasks.filter(status__in=['in_progress', 'resolved']).order_by('datetime_limit')
        context['tasks_created'] = user.tasks_created.exclude(status='closed')
        return context


class EventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'activism/events.html'
    context_object_name = 'events'
    
    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        context['events'] = context['events'].filter(status__in=['open'])
        return context


class EventView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'activism/event.html'
    fields = ('description', 'assignees')

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

    def form_invalid(self, form):
        super(EventView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'activism/task_create.html'
    form_class = TaskCreateForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'activism/task.html'
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        context['users'] = User.objects.all()
        return context

    def form_valid(self, form):
        result = super(TaskView, self).form_valid(form)
        task = self.get_object()
        if (task.assignees.all().count() >= task.number_of_assignees) and task.status == 'in_labor':
            task.status = 'in_progress'
        task.save()
        return result

    def form_invalid(self, form):
        super(TaskView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


class DoTaskView(SingleObjectMixin, LoginRequiredMixin, View):
    model = Task
    raise_exception = True

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user not in task.candidates.all() and request.user not in task.assignees.all():
            task.candidates.add(request.user)
            task.save()
        return HttpResponseRedirect(reverse('activism:index'))
