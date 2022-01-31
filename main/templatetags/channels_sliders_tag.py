from django import template
from main.models import (
    Channel
)

register = template.Library()

@register.simple_tag()
def sportchannels(sort):
    sort_list = sort.split(',')
    channels = []
    for i in sort_list:
        try:
            channels.append(Channel.objects.get(id=i, is_active=True))
        except Channel.DoesNotExist:
            pass
    return channels
@register.simple_tag()
def channelchannels(sort):
    sort_list = sort.split(',')
    channels = []
    for i in sort_list:
        try:
            channels.append(Channel.objects.get(id=i, is_active=True))
        except Channel.DoesNotExist:
            pass
    return channels
