from autocomplete_light import ModelForm, ModelChoiceField
from django.forms import HiddenInput, CharField
from django.contrib.auth.models import Group, User
from activism.models import Task, Event, AssigneeTask
import autocomplete_light

autocomplete_light.autodiscover()


class TaskCreateForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        if not Group.objects.get(name="Руководящая группа") in user.groups.all():
            self.fields['event'].queryset = user.events.filter(status='open')
            self.fields['event'].empty_label = None
        else:
            self.fields['event'].queryset = Event.objects.filter(status='open')

    class Meta:
        model = Task
        fields = ('event', 'sector', 'name', 'number_of_assignees', 'hours_predict')


class TaskForm(ModelForm):
    assignees_autocomplete = ModelChoiceField('UserAutocomplete', required=False)
    assignees = CharField(required=False)

    class Meta:
        model = Task
        fields = ('hours_predict', 'description', 'datetime_limit',
                  'candidates', 'number_of_assignees',
                  'event', 'rejected', 'sector')
        widgets = {
            'assignees': HiddenInput(),
        }

    def clean_assignees(self):
        return self.data['assignees'].split(',')[:-1]

    def save(self, commit=True):
        for pk in self.cleaned_data['assignees']:
            AssigneeTask.objects.get_or_create(task=self.instance, user=User.objects.get(pk=pk))
        AssigneeTask.objects.filter(task=self.instance)\
                            .exclude(user__pk__in=self.cleaned_data['assignees'])\
                            .delete()
        return super(TaskForm, self).save(commit)


class EventForm(ModelForm):
    assignees_autocomplete = ModelChoiceField('UserAutocomplete', required=False)

    class Meta:
        model = Event
        fields = ('description', 'assignees', 'date_held', 'sector')