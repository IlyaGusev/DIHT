from django.views.generic import DetailView, ListView
from activism.models import Event, Task
import logging
logger = logging.getLogger('DIHT.custom')


class IndexView(ListView):
    model = Event
    template_name = 'activism/activism.html'
    context_object_name = 'events'


class EventView(DetailView):
    model = Event
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'activism/event.html'
