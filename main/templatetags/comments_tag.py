from django import template
from users.models import Comment, CommentLike

register = template.Library()
@register.simple_tag()
def check_user_like(comment, user):
    if user.is_anonymous:
        return False
    try:
        cl = CommentLike.objects.get(user=user, comment=comment)
        return True
    except CommentLike.DoesNotExist:
        return False