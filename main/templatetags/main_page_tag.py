from django import template
from json import loads
from main.models import (
    Movie, Serie, Sport, ChannelProvider, Show, Adbanner, Channel
)

register = template.Library()


@register.simple_tag()
def bigslider(sort):
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
def newestmoviesslider(sort):
    sort = sort.split(',')
    clauses = ' '.join(["WHEN imdb_id='%s' THEN %s" % (pk, i) for i, pk in enumerate(sort)])
    ordering = 'CASE %s END' % clauses
    return Movie.objects.filter(imdb_id__in=sort, is_active=True).extra(
        select={'ordering': ordering}, order_by=('ordering',))


@register.simple_tag()
def sportvileslider(sort):
    sort = sort.split(',')
    clauses = ' '.join(["WHEN id=%s THEN %s" % (pk, i) for i, pk in enumerate(sort)])
    ordering = 'CASE %s END' % clauses
    return Sport.objects.filter(id__in=sort, is_active=True, live_ch=True).extra(
        select={'ordering': ordering}, order_by=('ordering',))


@register.simple_tag()
def popularchannellist(sort):
    sort = sort.split(',')
    clauses = ' '.join(["WHEN id=%s THEN %s" % (pk, i) for i, pk in enumerate(sort)])
    ordering = 'CASE %s END' % clauses
    return ChannelProvider.objects.filter(id__in=sort).extra(
        select={'ordering': ordering}, order_by=('ordering',))


@register.simple_tag()
def populartvshowsslider(sort):
    sort = sort.split(',')
    clauses = ' '.join(["WHEN imdb_id='%s' THEN %s" % (pk, i) for i, pk in enumerate(sort)])
    ordering = 'CASE %s END' % clauses
    return Show.objects.filter(imdb_id__in=sort, is_active=True).extra(
        select={'ordering': ordering}, order_by=('ordering',))