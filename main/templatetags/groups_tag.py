from django import template
# from users import

register = template.Library()

@register.simple_tag()
def get_groups_for_user():
    pass
    # return providers


