from users.models import UserWatchHisory, UserWatchList, UserFeedback
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


def add_model_to_history(user, model):
    model_type = ContentType.objects.get_for_model(model)
    try:
        history = UserWatchHisory.objects.get(user=user, content_type_id=model_type.id, object_id=model.id)
        history.date = now()
        history.save()

    except UserWatchHisory.DoesNotExist:
        history = UserWatchHisory(
            user=user,
            content_object=model
        )
        history.save()


def add_model_to_watchlist(user, model):
    model_type = ContentType.objects.get_for_model(model)
    try:
        watchlist = UserWatchList.objects.get(user=user, content_type_id=model_type.id, object_id=model.id)
        watchlist.delete()

    except UserWatchList.DoesNotExist:
        watchlist = UserWatchList(
            user=user,
            content_object=model
        )
        watchlist.save()


def get_object_in_watchlist(user, model):
    model_type = ContentType.objects.get_for_model(model)
    try:
        watchlist = UserWatchList.objects.get(user=user, content_type_id=model_type.id, object_id=model.id)
        return True
    except UserWatchList.DoesNotExist:
        return False


def save_feedback_from_user(user, message):
    try:
        cf = UserFeedback.objects.filter(user=user).order_by('-date')[0]
        if ((now() - cf.date).seconds / 60) < 5:
            print((now() - cf.date).seconds / 60)
            return False
    except UserFeedback.DoesNotExist:
        pass
    feedback = UserFeedback(
        user=user,
        text=message
    )
    feedback.save()
    return True


def remove_from_history_model(user, model):
    model_type = ContentType.objects.get_for_model(model)
    try:
        history = UserWatchHisory.objects.get(user=user, content_type_id=model_type.id, object_id=model.id)
        history.delete()

    except UserWatchHisory.DoesNotExist:
        return False
