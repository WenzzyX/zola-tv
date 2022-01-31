from users.models import UserSubscription

def get_subscriptions_for_user(user):
    try:
        return UserSubscription.objects.get(user=user)
    except UserSubscription.DoesNotExist:
        return False