from autocomplete_light import ModelForm, ModelChoiceField
from django.forms import HiddenInput, DateTimeInput
from django import forms
from activism.models import Task
import autocomplete_light

autocomplete_light.autodiscover()


class TaskForm(ModelForm):
    assignees_autocomplete = ModelChoiceField('UserAutocomplete', required=False)

    class Meta:
        model = Task
        fields = ('hours_predict', 'description', 'datetime_limit',
                  'assignees', 'candidates', 'number_of_assignees',
                  'event')


class TaskCreateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('event', 'name', 'number_of_assignees', 'hours_predict')