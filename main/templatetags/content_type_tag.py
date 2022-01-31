from django import template
from main.utils.UserLists import get_object_in_watchlist

register = template.Library()

@register.simple_tag()
def check_added_to_watchlist(user, model):
    if not user.is_anonymous:
        return get_object_in_watchlist(user, model)
    else:
        return False