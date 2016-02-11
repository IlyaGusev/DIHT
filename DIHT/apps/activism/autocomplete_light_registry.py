# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания:
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Настройка автодополнения по имени и фамилии в autocomplete_light в модуле активистов.
"""
import autocomplete_light
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from taggit.models import Tag


class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    model = User
    search_fields = ['^first_name', '^last_name']
    choices = User.objects.filter(groups__name__in=['Активисты'])
    attrs = {
        'data-autcomplete-minimum-characters': 0,
        'placeholder': 'Имя или фамилия',
    }

    # Переопределил из autocomplete_light.autocomplete.base
    def choice_label(self, choice):
        return force_text(choice.get_full_name())


autocomplete_light.register(UserAutocomplete)
autocomplete_light.register(Tag)