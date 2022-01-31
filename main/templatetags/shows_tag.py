from django import template
from main.models import (
    Show, Showlist
)

register = template.Library()

@register.simple_tag()
def werecomendedslider(sort):
    sort_list = sort.split(',')
    shows = []
    for i in sort_list:
        try:
            shows.append(Show.objects.get(imdb_id=i, is_active=True))
        except Show.DoesNotExist:
            pass
    return shows

@register.simple_tag()
def toplistsslider(sort):
    sort_list = sort.split(',')
    lists = []
    for i in sort_list:
        try:
            lists.append(Showlist.objects.get(id=i))
        except Showlist.DoesNotExist:
            pass
    return lists

@register.simple_tag()
def getEpisodes(season):
    episodes = season.seas.all().order_by('episode')
    return episodes