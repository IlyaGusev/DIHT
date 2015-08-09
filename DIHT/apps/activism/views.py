from django.views.generic import ListView, View
from braces.views import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from activism.models import Event, Task
from django.http import JsonResponse
import logging
logger = logging.getLogger('DIHT.custom')


class IndexView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'activism/dashboard.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(status__in=['in_labor'])
        return context


class EventView(LoginRequiredMixin, UpdateView):
    model = Event
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'activism/event.html'
    fields = ('description', 'assignees')

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

    def form_invalid(self, form):
        super(EventView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


class TaskView(LoginRequiredMixin, UpdateView):
    model = Task
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'activism/task.html'
    fields = ('hours_predict', 'description', 'datetime_limit',
              'assignees', 'candidates', 'number_of_assignees',
              'event')

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
    slug_field = 'id'
    slug_url_kwarg = 'id'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user not in task.candidates.all() and request.user not in task.assignees.all():
            task.candidates.add(request.user)
            task.save()
        return HttpResponseRedirect(reverse('activism:index'))
