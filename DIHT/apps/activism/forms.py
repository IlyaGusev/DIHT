from autocomplete_light import ModelForm, ModelChoiceField
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