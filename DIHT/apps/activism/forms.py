from autocomplete_light import ModelForm, ModelChoiceField, MultipleChoiceField
from django.forms import HiddenInput
from django.contrib.auth.models import Group
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
        fields = ('event', 'name', 'number_of_assignees', 'hours_predict')


class TaskForm(ModelForm):
    assignees_autocomplete = ModelChoiceField('UserAutocomplete', required=False)

    class Meta:
        model = Task
        fields = ('hours_predict', 'description', 'datetime_limit',
                  'assignees', 'candidates', 'number_of_assignees',
                  'event', 'rejected')

    def save(self, commit=True):
        for pk in self['assignees']:
            participate = AssigneeTask.objects.get_or_create(task=self.instance.pk, user=pk)
        return super(TaskForm, self).save(commit)



class EventForm(ModelForm):
    assignees_autocomplete = ModelChoiceField('UserAutocomplete', required=False)

    class Meta:
        model = Event
        fields = ('description', 'assignees', 'date_held')