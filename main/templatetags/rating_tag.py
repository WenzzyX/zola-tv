from django import template
from main.utils.UserRating import get_rating_for_model, check_user_rated_model
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag()
def get_rating(object):
    return get_rating_for_model(object)


@register.simple_tag()
def check_rating_user(object, user):
    if not user.is_anonymous:
        return check_user_rated_model(object, user)
    return False


@register.simple_tag()
def get_ct_model(model):
    model_type = ContentType.objects.get_for_model(model)
    return model_type.id
