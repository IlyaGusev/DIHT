# -*- coding: utf-8 -*-
from django import template
from math import ceil
register = template.Library()


# Деление списка на n частей
@register.filter
def partition(thelist, n):
    try:
        n = int(n)
        thelist = list(thelist)
    except (ValueError, TypeError):
        return [thelist]
    p = ceil(len(thelist) / n)
    return [thelist[p*i:p*(i+1)] for i in range(n - 1)] + [thelist[p*(n-1):]]
