from django import template
from main.utils.UserLists import get_object_in_watchlist
from main.models import Channel
from django.contrib.contenttypes.fields import ContentType
register = template.Library()

@register.simple_tag()
def get_all_watch_list(user):
    return [obj.content_object for obj in user.watchlist.all().order_by('-date')]

@register.simple_tag()
def get_all_channels_list(user):
    return [obj.content_object for obj in user.watchlist.filter(content_type=ContentType.objects.get_for_model(Channel)).order_by('-date')]

@register.simple_tag()
def get_all_watch_history(user):
    return [obj.content_object for obj in user.watchhistory.all().order_by('-date')]