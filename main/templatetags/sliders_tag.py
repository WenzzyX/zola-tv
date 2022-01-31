from django import template
from json import loads
from main.models import (
    Movie, Serie, Sport, ChannelProvider, Show, Adbanner, Channel, Movielist, Serielist, Showlist, Sportlist,
    Channellist
)

register = template.Library()


def get_ordering(sort, sort_field):
    clauses = ' '.join(["WHEN %s='%s' THEN %s" % (sort_field, pk, i) for i, pk in enumerate(sort)])
    return 'CASE %s END' % clauses


@register.simple_tag()
def main_big_slider(sort):
    sort_list = sort.split(",")
    result = []
    for sort_element in sort_list:
        sort_dict = loads(sort_element)
        key = list(sort_dict.keys())[0]
        try:
            switch = (
                    (key == "mo" and result.append(
                        {
                            "element": Movie.objects.get(imdb_id=sort_dict[key], is_active=True),
                            "type": key
                        }
                    )) or
                    (key == "se" and result.append(
                        {
                            "element": Serie.objects.get(imdb_id=sort_dict[key], is_active=True),
                            "type": key
                        }
                    )) or
                    (key == "sh" and result.append(
                        {
                            "element": Show.objects.get(imdb_id=sort_dict[key], is_active=True),
                            "type": key
                        }
                    )) or
                    (key == "ch" and result.append(
                        {
                            "element": Channel.objects.get(id=sort_dict[key], is_active=True),
                            "type": key
                        }
                    ))
            )
        except (Movie.DoesNotExist, Serie.DoesNotExist, Show.DoesNotExist, Channel.DoesNotExist):
            pass
    return result


@register.simple_tag()
def movie_slider(sort):
    sort = sort.split(',')
    return Movie.objects.filter(imdb_id__in=sort, is_active=True).extra(
        select={'ordering': get_ordering(sort, 'imdb_id')}, order_by=('ordering',))


@register.simple_tag()
def serie_slider(sort):
    sort = sort.split(',')
    return Serie.objects.filter(imdb_id__in=sort, is_active=True).extra(
        select={'ordering': get_ordering(sort, 'imdb_id')}, order_by=('ordering',))


@register.simple_tag()
def show_slider(sort):
    sort = sort.split(',')
    return Show.objects.filter(imdb_id__in=sort, is_active=True).extra(
        select={'ordering': get_ordering(sort, 'imdb_id')}, order_by=('ordering',))


@register.simple_tag()
def sport_slider(sort):
    sort = sort.split(',')
    return Sport.objects.filter(id__in=sort, is_active=True, live_ch=True).extra(
        select={'ordering': get_ordering(sort, 'id')}, order_by=('ordering',))


@register.simple_tag()
def channel_list(sort):
    sort = sort.split(',')
    return Channel.objects.filter(id__in=sort).extra(
        select={'ordering': get_ordering(sort, 'id')}, order_by=('ordering',))


@register.simple_tag()
def channel_provider_list(sort):
    sort = sort.split(',')
    return ChannelProvider.objects.filter(id__in=sort).extra(
        select={'ordering': get_ordering(sort, 'id')}, order_by=('ordering',))


@register.simple_tag()
def movie_toplist_slider(sort):
    sort = sort.split(',')
    return Movielist.objects.filter(id__in=sort).extra(
        select={'ordering': get_ordering(sort, 'id')}, order_by=('ordering',))


@register.simple_tag()
def serie_toplist_slider(sort):
    sort = sort.split(',')
    return Serielist.objects.filter(id__in=sort).extra(
        select={'ordering': get_ordering(sort, 'id')}, order_by=('ordering',))


@register.simple_tag()
def show_toplist_slider(sort):
    sort = sort.split(',')
    return Showlist.objects.filter(id__in=sort).extra(
        select={'ordering': get_ordering(sort, 'id')}, order_by=('ordering',))


@register.simple_tag()
def channel_toplist_slider(sort):
    sort = sort.split(',')
    return Channellist.objects.filter(id__in=sort).extra(
        select={'ordering': get_ordering(sort, 'id')}, order_by=('ordering',))
