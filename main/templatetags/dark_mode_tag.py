from django import template

register = template.Library()

@register.simple_tag()
def set_dark(user):
    if not user.is_anonymous and user.user_profile.first():
        if user.user_profile.first().dark_mode:
            return True
    return False