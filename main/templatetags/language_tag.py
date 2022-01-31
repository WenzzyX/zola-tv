from django import template
from main.models import MovieAltLang, SerieEpAltLang, SerieSeason, ShowEpAltLang, ShowSeason

register = template.Library()

@register.simple_tag()
def get_movie_alt_langs(object):
    altLangs = MovieAltLang.objects.filter(movie=object)
    return altLangs

@register.simple_tag()
def get_serie_alt_langs(object):
    season = SerieSeason.objects.filter(serie=object).first()
    if season != None:
        episode = season.seas.first()
        altLangs = SerieEpAltLang.objects.filter(episode=episode)
        return altLangs
    else:
        return []

@register.simple_tag()
def get_show_alt_langs(object):
    season = ShowSeason.objects.filter(show=object).first()
    if season != None:
        episode = season.seas.first()
        altLangs = ShowEpAltLang.objects.filter(episode=episode)
        return altLangs
    else:
        return []