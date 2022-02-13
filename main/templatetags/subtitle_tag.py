from django import template
import re
from main.models import (
    Language, Subtitle
)

register = template.Library()

@register.simple_tag()
def get_subtitles(sub_urls):
    if len(sub_urls) < 4:
        return ''
    sub_list = sub_urls.split(',')
    final_links = []
    for link in sub_list:
        print(link)
        match = re.search(r'/(\w*.\w*)$', link).group(0).strip('/')
        lang_iso3 = match.split('_')
        if len(lang_iso3) == 1:
            lang_iso3 = 'eng'
        else:
            lang_iso3 = lang_iso3[0]
        try:
            lang = Language.objects.get(iso3=lang_iso3)
            final_links.append(f'[{lang.name}]{link}')
        except Language.DoesNotExist:
            final_links.append(f'[{lang_iso3}]{link}')
            pass
    return ','.join(final_links)

@register.simple_tag()
def get_25_subs(name):
    return Subtitle.objects.filter(file_name__icontains=name)[:25]