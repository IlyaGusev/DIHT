# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания:
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Формы, связанные заданиями, мероприятиями, очками роста.
"""
from django.forms import MultipleChoiceField, IntegerField, CharField
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from autocomplete_light import ModelForm, ModelChoiceField
from autocomplete_light.contrib.taggit_field import TaggitField, TaggitWidget
from activism.models import Task, Event, AssigneeTask, ResponsibleEvent
from activism.utils import global_checks


class OverwriteOnlyModelFormMixin(object):
    """
    Delete POST keys that were not actually found in the POST dict
    to prevent accidental overwriting of fields due to missing POST data.
    Mixin для поддержки перезаписи полей. Без него незаполенные поля считаются пустыми.
    """
    def __init__(self, *args, **kwargs):
        super(OverwriteOnlyModelFormMixin, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].required = False

    def clean(self):
        cleaned_data = super(OverwriteOnlyModelFormMixin, self).clean()
        # Записываем в data новые поля
        data = {}
        for field in cleaned_data.keys():
            if field in self.data:
                data[field] = cleaned_data[field]
        # Запоминаем новые поля
        obj = get_object_or_404(self._meta.model, pk=self.instance.pk)
        # Достаём старые поля и обновляем их
        model_data = obj.__dict__
        model_data.update(data)
        return model_data


class TaskCreateForm(ModelForm):
    """
    Форма модали для создания задачи. С разрешением can_choose_events в выпадающем списке
    показываются все мероприятия, без него - только те, за которые юзер ответственен.
    """
    def __init__(self, user, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        checks = global_checks(user)
        if not checks['can_choose_all_events']:
            self.fields['event'].queryset = Event.objects.filter(pk__in=user.event_responsible
                                                                            .filter(event__status='open')
                                                                            .values_list('event', flat=True))
            self.fields['event'].empty_label = None
        else:
            self.fields['event'].queryset = Event.objects.filter(status='open')

    class Meta:
        model = Task
        fields = ('event', 'sector', 'name', 'number_of_assignees', 'hours_predict')


class TaskForm(OverwriteOnlyModelFormMixin, ModelForm):
    """
    Форма для редактирования задачи.
    Все эти clean нужны из-за того, что Django по умолчанию не принимает массивы как MultipleChoice.
    Для того, чтобы это работало, в __init__ все поля генерируются динамически.
    """
    assignees_autocomplete = ModelChoiceField('UserAutocomplete', required=False)
    responsible_autocomplete = ModelChoiceField('UserAutocomplete', required=False)
    tags = TaggitField(widget=TaggitWidget('TagAutocomplete'), required=False)

    class Meta:
        model = Task
        fields = ('hours_predict', 'description', 'datetime_limit',
                  'candidates', 'number_of_assignees', 'responsible',
                  'event', 'rejected', 'sector', 'tags', 'name')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assignees_pk'] = MultipleChoiceField(choices=[(i, i) for i in User.objects.all().values_list('pk', flat=True)] +
                                                                  [('None', 'None'), ], required=False)
        self.fields['candidates'] = MultipleChoiceField(choices=[(i, i) for i in User.objects.all().values_list('pk', flat=True)] +
                                                                [('None', 'None'), ], required=False)
        self.fields['responsible'] = MultipleChoiceField(choices=[(i, i) for i in User.objects.all().values_list('pk', flat=True)] +
                                                                 [('None', 'None'), ], required=False)

    def clean_assignees_pk(self):
        if self.data.get('assignees_pk') is not None:
            if self.data['assignees_pk'] == 'None':
                return []
            return self.cleaned_data['assignees_pk']
        return None

    def clean_responsible(self):
        if self.data.get('responsible') is not None:
            if self.data['responsible'] == 'None':
                return []
            return self.cleaned_data['responsible']
        return None

    def clean_candidates(self):
        if self.data.get('candidates') is not None:
            if self.data['candidates'] == 'None':
                return []
            return self.cleaned_data['candidates']
        return None

    def save(self, commit=True):
        # Для поддержки добавления и удаления назначенных
        if self.cleaned_data.get('assignees_pk') is not None:
            for pk in self.cleaned_data['assignees_pk']:
                AssigneeTask.objects.get_or_create(task=self.instance, user=User.objects.get(pk=pk))
            AssigneeTask.objects.filter(task=self.instance)\
                                .exclude(user__pk__in=self.cleaned_data['assignees_pk'])\
                                .delete()
        return super(TaskForm, self).save(commit)


class EventForm(OverwriteOnlyModelFormMixin, ModelForm):
    """
    Форма для редактирования мероприятия.
    Хаки аналогичны форме задачи.
    """
    responsible_autocomplete = ModelChoiceField('UserAutocomplete', required=False)

    class Meta:
        model = Event
        fields = ('description', 'date_held', 'sector')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['responsible'] = MultipleChoiceField(choices=[(i, i) for i in User.objects.all().values_list('pk', flat=True)] +
                                                                 [('None', 'None'), ], required=False)

    def clean_responsible(self):
        if self.data.get('responsible') is not None:
            if self.data['responsible'] == 'None':
                return []
            return self.cleaned_data['responsible']
        return None

    def save(self, commit=True):
        if self.cleaned_data.get('responsible') is not None:
            for pk in self.cleaned_data['responsible']:
                ResponsibleEvent.objects.get_or_create(event=self.instance, user=User.objects.get(pk=pk))
            ResponsibleEvent.objects.filter(event=self.instance)\
                                    .exclude(user__pk__in=self.cleaned_data['responsible'])\
                                    .delete()
        return super(EventForm, self).save(commit)


class PointForm(ModelForm):
    """
    Форма для добавления очков роста.
    ModelForm и пустой fields для простоты submit'а.
    """
    amount = IntegerField(min_value=0, max_value=10000, label="Количество")
    description = CharField(label="Обоснование")

    class Meta:
        model = User
        fields = []