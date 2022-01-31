from users.models import Comment, CommentLike
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


def safe_query(q: str):
    return q.strip()


def save_comment_for_model(user, model, query):
    model_type = ContentType.objects.get_for_model(model)
    try:
        cf = Comment.objects.filter(user=user, content_type_id=model_type.id, object_id=model.id).order_by('-date')[0]
        if ((now() - cf.date).seconds / 60) < 5:
            print((now() - cf.date).seconds / 60)
            return False
    except (Comment.DoesNotExist, IndexError):
        pass
    ncomment = Comment(
        user=user,
        text=safe_query(query),
        content_object=model
    )
    ncomment.save()
    return True


def set_like_for_comment(user, id):
    try:
        comment = Comment.objects.get(id=id)
        try:
            get_cl = CommentLike.objects.get(user=user, comment=comment)
            get_cl.delete()
            return True
        except CommentLike.DoesNotExist:
            cl = CommentLike(
                user=user,
                comment=comment
            )
            cl.save()
            return True
    except Comment.DoesNotExist:
        return False
