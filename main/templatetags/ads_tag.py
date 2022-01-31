from django import template
from main.models import (
    Adbanner
)

register = template.Library()

@register.simple_tag()
def get_ad(banner_sort):
    banner = ''
    try:
        banner = Adbanner.objects.get(id=int(banner_sort))
    except Adbanner.DoesNotExist:
        pass
    return banner