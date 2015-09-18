from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group


class GymView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(GymView, self).get_context_data(**kwargs)
        if Group.objects.filter(name="Ответственные за качалку").exists():
            context['charge_gym'] = Group.objects.get(name="Ответственные за качалку").user_set.all()
        return context