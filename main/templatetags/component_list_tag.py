from django import template
from django.shortcuts import Http404
from main.models import (
    Movie, Serie, Sport, Channel, ChannelProvider, Show,
    Movielist, Serielist, Sportlist, Showlist, Channellist
)

register = template.Library()


@register.simple_tag()
def componentlist(component):

    try:
        sort = set(int(x) for x in component.sort_method.split(','))
    except ValueError:
        print("ERR1")
        raise Http404("Compilation not found!")
    sort = component.sort_method.split(',')

    try:
        result_dict = {
            component.handler == "1": Movie.objects.filter(imdb_id__in=sort, is_active=True),
            component.handler == "2": Serie.objects.filter(imdb_id__in=sort, is_active=True),
            component.handler == "3": Sport.objects.filter(id__in=sort, is_active=True),
            component.handler == "4": ChannelProvider.objects.filter(id__in=sort),
            component.handler == "5": Channel.objects.filter(id__in=sort, is_active=True),
            component.handler == "6": Show.objects.filter(imdb_id__in=sort, is_active=True),
            component.handler == "7": Movielist.objects.filter(id__in=sort),
            component.handler == "8": Serielist.objects.filter(id__in=sort),
            component.handler == "9": Sportlist.objects.filter(id__in=sort),
            component.handler == "10": Showlist.objects.filter(id__in=sort),
            component.handler == "11": Channellist.objects.filter(id__in=sort),
        }[True]
    except (KeyError, Movie.DoesNotExist, Serie.DoesNotExist, Sport.DoesNotExist, ChannelProvider.DoesNotExist,
            Channel.DoesNotExist,
            Show.DoesNotExist, Movielist.DoesNotExist, Sportlist.DoesNotExist, Sportlist.DoesNotExist,
            Showlist.DoesNotExist):
        print("ERR2")
        raise Http404("Compilation not found!")
    # print(result_dict)
    try:
        template = {
            isinstance(result_dict[0], Serie) or isinstance(result_dict[0], Show): 2,
            isinstance(result_dict[0], Sport): 3,
            isinstance(result_dict[0], Movielist) or isinstance(result_dict[0], Serielist) or isinstance(result_dict[0],Sportlist) or isinstance(result_dict[0], Showlist) or isinstance(result_dict[0], Channel) or isinstance(result_dict[0],ChannelProvider) or isinstance(result_dict[0],Channellist): 4,
        }[True]
    except KeyError:
        template = 1

    try:
        page = {
            isinstance(result_dict[0], Movie): "movie-page",
            isinstance(result_dict[0], Serie): "serie-page",
            isinstance(result_dict[0], Sport): "sport-page",
            isinstance(result_dict[0], Show): "show-page",
            isinstance(result_dict[0], Channel): "channel-page",
            isinstance(result_dict[0], ChannelProvider): "provider-page",

            isinstance(result_dict[0], Movielist): "movie-list-page",
            isinstance(result_dict[0], Serielist): "serie-list-page",
            isinstance(result_dict[0], Sportlist): "sport-list-page",
            isinstance(result_dict[0], Showlist): "show-list-page",
            isinstance(result_dict[0], Channellist): "channel-list-page",
        }[True]
    except KeyError:
        print("ERR3")
        raise Http404("Compilation not found!")
    return {
        "elements": result_dict,
        "page": page,
        "template": template
    }
