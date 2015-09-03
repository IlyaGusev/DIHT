import autocomplete_light
from django.contrib.auth.models import User
from django.utils.encoding import force_text


class ProfileAutocomplete(autocomplete_light.AutocompleteModelBase):
    model = User
    search_fields = ['^first_name', '^last_name']
    attrs = {
        'data-autcomplete-minimum-characters': 0,
        'placeholder': 'Имя или фамилия',
    }

    # Переопределил из autocomplete_light.autocomplete.base
    def choice_label(self, choice):
        return force_text(choice.get_full_name())


autocomplete_light.register(ProfileAutocomplete)