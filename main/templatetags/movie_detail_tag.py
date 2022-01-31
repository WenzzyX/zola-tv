from django import template
from json import loads
from main.models import (
    Movie, Serie, Sport, ChannelProvider, Show, Adbanner
)

register = template.Library()


@register.simple_tag()
def similarmovies(sort):
    sort_list = sort.split(',')
    movies = []
    for i in sort_list:
        try:
            movies.append(Movie.objects.get(imdb_id=i, is_active=True))
        except Movie.DoesNotExist:
            pass
    return movies
