from django import template
from main.models import Channel

register = template.Library()

@register.simple_tag()
def get_channels_for_provider(prov):
   try:
      objs = Channel.objects.filter(provider=prov, is_active=True)
      return objs
   except:
      return None