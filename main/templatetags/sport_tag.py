from django import template
from main.models import (
    Sport
)

register = template.Library()

@register.simple_tag()
def livelist(sort):
    sort_list = sort.split(',')
    sports = []
    for i in sort_list:
        try:
            sports.append(Sport.objects.get(id=i, live_ch=True, is_active=True))
        except Sport.DoesNotExist:
            pass
    return sports

@register.simple_tag()
def matcheslist(sort):
    sort_list = sort.split(',')
    sports = []
    for i in sort_list:
        try:
            sports.append(Sport.objects.get(id=i, is_active=True))
        except Sport.DoesNotExist:
            pass
    return sports