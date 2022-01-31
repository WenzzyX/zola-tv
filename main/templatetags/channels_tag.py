from django import template
from main.models import (
    Channel, ChannelProvider, Adbanner, Channellist
)

register = template.Library()

@register.simple_tag()
def providerlist(sort):
    sort_list = sort.split(',')
    providers = []
    for i in sort_list:
        try:
            providers.append(ChannelProvider.objects.get(id=i))
        except ChannelProvider.DoesNotExist:
            pass
    return providers


@register.simple_tag()
def allproviderlist(sort):
    sort_list = sort.split(',')
    providers = []
    for i in sort_list:
        try:
            providers.append(ChannelProvider.objects.get(id=i))
        except ChannelProvider.DoesNotExist:
            pass
    return providers

@register.simple_tag()
def werecomendedlist(sort):
    sort_list = sort.split(',')
    channels = []
    for i in sort_list:
        try:
            channels.append(Channel.objects.get(id=i, is_active=True))
        except Channel.DoesNotExist:
            pass
    return channels


@register.simple_tag()
def adsbanner(sort):
    # sort_list = sort.split(',')
    # banner = []
    try:
        banner = Adbanner.objects.get(id=sort)
        return banner
    except Adbanner.DoesNotExist:
        pass
    return []


@register.simple_tag()
def toplistsslider(sort):
    sort_list = sort.split(',')
    lists = []
    for i in sort_list:
        try:
            lists.append(Channellist.objects.get(id=i))
        except Channellist.DoesNotExist:
            pass
    return lists
