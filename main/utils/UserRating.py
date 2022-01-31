from users.models import Rating
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


def get_rating_for_model(model):
    s_rationg = model.get_rating()
    if s_rationg:
        return s_rationg
    else:
        try:
            rating = float("%.1f" % (model.imdb_rating + 0.7))
            if rating > 10:
                rating = rating - (rating % 10)
        except Exception as e:
            pass
            rating = 5.5
    return {
        "grade": rating,
        "based": model.user_rating_q
    }

def get_rating_for_ct_model(model_id, ct_id):
    try:
        model = ContentType.objects.get(pk=ct_id).model_class().objects.get(id=model_id)
    except Exception as e:
        return False
    s_rationg = model.get_rating()
    print(s_rationg)
    if s_rationg:
        return s_rationg
    else:
        rating = float("%.1f" % (model.imdb_rating + 0.7))
        if rating > 10:
            rating = rating - (rating % 10)
    return {
        "grade": rating,
        "based": 0
    }


def set_rating_for_model(model_id, ct_id, grade, user):
    try:
        model = ContentType.objects.get(pk=ct_id).model_class().objects.get(id=model_id)
        try:
            this_model = Rating.objects.get(user=user, content_type_id=ct_id, object_id=model_id)
            model.user_rating_all = (model.user_rating_all - this_model.grade) + int(grade)
            model.save()
            this_model.grade = int(grade)
            this_model.save()
        except Rating.DoesNotExist:
            new_rating = Rating(
                user=user,
                grade=grade,
                content_object=model
            )
            model.user_rating_all += int(grade)
            model.user_rating_q += 1
            model.save()
            new_rating.save()
        return True
    except Exception as e:
        return False

def check_user_rated_model(model, user):
    model_type = ContentType.objects.get_for_model(model)
    try:
        u_rating = Rating.objects.get(user=user, content_type_id=model_type.id, object_id=model.id)
        return u_rating.grade
    except Rating.DoesNotExist:
        return False
