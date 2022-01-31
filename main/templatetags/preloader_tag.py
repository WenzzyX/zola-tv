from django import template
from main.models import (
    Component, Adbanner
)

register = template.Library()


@register.simple_tag()
def adsbanner():
    component_id = 7 # CONST !!!
    try:
        component = Component.objects.get(id=component_id)
        return component
    except Component.DoesNotExist:
        pass
    return None

