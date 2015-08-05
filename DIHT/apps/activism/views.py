from django.views.generic import DetailView, ListView, View
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from activism.models import Event, Task
import logging
logger = logging.getLogger('DIHT.custom')


class IndexView(ListView):
    model = Task
    template_name = 'activism/dashboard.html'
    context_object_name = 'tasks'



class EventView(DetailView):
    model = Event
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'activism/event.html'


class TaskView(DetailView):
    model = Task
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'activism/task.html'


class DoTaskView(SingleObjectMixin, View):
    model = Task
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        task.candidates.add(request.user)
        task.save()
        return HttpResponseRedirect(reverse('activism:index'))
