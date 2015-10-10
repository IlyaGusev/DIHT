from django.contrib.auth.models import Group
from activism.models import Task


def global_checks(user, obj=None):
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


def get_level(user):
    if Group.objects.get(name="Руководящая группа") in user.groups.all():
        return {'sign': 'Руководящая группа', 'coef': 0}

    hours = sum(user.participated.filter(task__status__in=['closed']).values_list('hours', flat=True))
    gp = hours // 10 + sum(user.point_operations.all().values_list('amount', flat=True))

    if gp < 4:
        return {'sign': 'Активист-новичок', 'coef': 0}
    elif gp < 16:
        return {'sign': 'Активист', 'coef': 1}
    elif gp < 35:
        return {'sign': 'Активист-организатор', 'coef': 1.7}
    elif gp < 70:
        return {'sign': 'Активист-лидер', 'coef': 2.4}
    else:
        return {'sign': 'Активист-руководитель', 'coef': 4}