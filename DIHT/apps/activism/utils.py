# -*- coding: utf-8 -*-
"""
    Авторы: Гусев Илья
    Дата создания:
    Версия Python: 3.4
    Версия Django: 1.8.5
    Описание:
        Глобальные функции для работы с моделем активстов.
"""
from django.contrib.auth.models import Group
from activism.models import Task


def global_checks(user, obj=None):
    """
    Функция, проверяющая права пользователя user для объекта obj.
    Возвращает словарь вида {"право": True/False, ...}.
    """
    context = dict()
    context['is_superuser'] = user.is_superuser
    context['is_charge'] = Group.objects.get(name="Ответственные за активистов") in user.groups.all()
    context['is_main'] = Group.objects.get(name="Руководящая группа") in user.groups.all()
    context['can_all'] = context['is_charge'] or context['is_superuser']
    context['has_events'] = user.event_responsible.filter(event__status='open').count() != 0
    context['can_create_tasks'] = (context['has_events'] or
                                   context['is_charge'] or
                                   context['is_superuser'] or
                                   context['is_main'])
    context['can_choose_all_events'] = context['is_main'] or context['can_all']
    context['can_manage'] = context['is_charge'] or context['is_superuser']
    if obj is not None:
        context['is_responsible'] = (user in obj.responsible.all())
        context['can_manage'] = context['can_manage'] or context['is_responsible']
        if hasattr(obj, 'sector'):
            if obj.sector is not None:
                context['is_sector_main'] = (obj.sector.main == user)
                context['can_manage'] = context['can_manage'] or context['is_sector_main']
        if isinstance(obj, Task):
            context['is_assignee'] = user in obj.assignees.all()
    return context

def get_level_by_num(num):
    """
     Функция, рассчитывающая уровень по его номеру.
    """
    if num == -1:
        return {'sign': 'Руководящая группа', 'coef': 0, 'is_beginner' : True, 'num' : -1}
    elif num == 0:
        return {'sign': 'Активист-новичок', 'coef': 1, 'is_beginner' : True, 'num' : 0}
    elif num == 1:
        return {'sign': 'Активист', 'coef': 1, 'is_beginner' : False, 'num' : 1}
    elif num == 2:
        return {'sign': 'Активист-организатор', 'coef': 1.7, 'is_beginner' : False, 'num' : 2}
    elif num == 3:
        return {'sign': 'Активист-лидер', 'coef': 2.4, 'is_beginner' : False, 'num' : 3}
    elif num == 4:
        return {'sign': 'Активист-руководитель', 'coef': 4, 'is_beginner' : False, 'num' : 4}
    else:
        return {'sign': 'Почётный активист студсовета ФИВТ', 'coef': 4, 'is_beginner' : False, 'num' : 5}

def get_level_by_point_sum(gp):
    gp += 1e-4
    if gp < 4:
        return get_level_by_num(0)
    elif gp < 16:
        return get_level_by_num(1)
    elif gp < 35:
        return get_level_by_num(2)
    elif gp < 70:
        return get_level_by_num(3)
    else:
        return get_level_by_num(4)


def get_level(user):
    """
    Функция, рассчитывающая текущий уровень активиста user.
    """
    if Group.objects.get(name="Руководящая группа") in user.groups.all():
        return get_level_by_num(-1)

    return get_level_by_point_sum(user.profile.experience)