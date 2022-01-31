from django import template
from main.models import (
    Serie
)

register = template.Library()

@register.simple_tag()
def bigslider(sort):
    sort_list = sort.split(',')
    series = []
    for i in sort_list:
        try:
            series.append(Serie.objects.get(imdb_id=i, is_active=True))
        except Serie.DoesNotExist:
            pass
    return series

@register.simple_tag()
def newestseriesslider(sort):
    sort_list = sort.split(',')
    series = []
    for i in sort_list:
        try:
            series.append(Serie.objects.get(imdb_id=i, is_active=True))
        except Serie.DoesNotExist:
            pass
    return series

@register.simple_tag()
def werecomendedslider(sort):
    sort_list = sort.split(',')
    series = []
    for i in sort_list:
        try:
            series.append(Serie.objects.get(imdb_id=i, is_active=True))
        except Serie.DoesNotExist:
            pass
    return series

@register.simple_tag()
def genreslider(sort):
    sort_list = sort.split(',')
    series = []
    for i in sort_list:
        try:
            series.append(Serie.objects.get(imdb_id=i, is_active=True))
        except Serie.DoesNotExist:
            pass
    return series


@register.simple_tag()
def getEpisodes(season):
    episodes = season.seas.all().order_by('episode')
    return episodes