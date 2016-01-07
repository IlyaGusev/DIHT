# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.models import Group
register = template.Library()


# Проверка на принадлежность пользователя к определённой группе на этапе отображения
@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False