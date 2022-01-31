from django import template
from main.models import (
    Movie, Serie, Sport, Show, Channel
)

register = template.Library()


@register.simple_tag()
def get_movies_f_list(sort):
    return Movie.objects.filter(imdb_id__in=sort.split(','), is_active=True)


@register.simple_tag()
def get_series_f_list(sort):
    return Serie.objects.filter(imdb_id__in=sort.split(','), is_active=True)


@register.simple_tag()
def get_show_f_list(sort):
    return Show.objects.filter(imdb_id__in=sort.split(','), is_active=True)


@register.simple_tag()
def get_channels_f_list(sort):
    return Channel.objects.filter(id__in=sort.split(','), is_active=True)


@register.simple_tag()
def get_sport_f_list(sort):
    return Sport.objects.filter(id__in=sort.split(','), is_active=True)
