from django import template
from main.models import (
    Movie, Movielist
)

register = template.Library()

@register.simple_tag()
def bigslider(sort):
    sort_list = sort.split(',')
    movies = []
    for i in sort_list:
        try:
            movies.append(Movie.objects.get(imdb_id=i, is_active=True))
        except Movie.DoesNotExist:
            pass
    return movies

@register.simple_tag()
def newestmoviesslider(sort):
    sort_list = sort.split(',')
    movies = []
    for i in sort_list:
        try:
            movies.append(Movie.objects.get(imdb_id=i, is_active=True))
        except Movie.DoesNotExist:
            pass
    return movies

@register.simple_tag()
def toplistsslider(sort):
    sort_list = sort.split(',')
    lists = []
    for i in sort_list:
        try:
            lists.append(Movielist.objects.get(id=i))
        except Movielist.DoesNotExist:
            pass
    return lists

@register.simple_tag()
def recomendedtoyouslider(sort):
    sort_list = sort.split(',')
    movies = []
    for i in sort_list:
        try:
            movies.append(Movie.objects.get(imdb_id=i, is_active=True))
        except Movie.DoesNotExist:
            pass
    return movies

@register.simple_tag()
def genreslider(sort):
    sort_list = sort.split(',')
    movies = []
    for i in sort_list:
        try:
            movies.append(Movie.objects.get(imdb_id=i, is_active=True))
        except Movie.DoesNotExist:
            pass
    return movies