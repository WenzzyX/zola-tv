from django import template
from django.conf import settings
from main.models import Setting

register = template.Library()


@register.simple_tag()
def get_settings():
    result = {}
    result['SHOW_HEADERS'] = settings.SHOW_HEADERS
    result['SHOW_FOOTERS'] = settings.SHOW_FOOTERS
    result['ITS_APP'] = settings.ITS_APP
    result['CLON_APP'] = settings.CLON_APP
    result['time_to_dapp'] = 600
    try:
        result['time_to_dapp'] = Setting.objects.get(t_id=1).value
    except:
        pass
    return result
