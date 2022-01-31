from django.db.models import Q
from users.models import CustomUser
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Exists, OuterRef, Q
# MyUser = get_user_model()

UserModel = get_user_model()


class PhoneOrEmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(email=username) | Q(email=username.lower()) | Q(phone=username))
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except UserModel.DoesNotExist as e:
            UserModel().set_password(password)

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
# class PhoneOrEmailBackend(object):
#     def authenticate(self, username=None, password=None):
#         my_user_model = get_user_model()
#         print(1)
#         try:
#             user = my_user_model.objects.get(email=username)
#             if user.check_password(password):
#                 return user  # return user on valid credentials
#         except my_user_model.DoesNotExist:
#             return None  # return None if custom user model does not exist
#         except:
#             return None  # return None in case of other exceptions
#
#     def get_user(self, user_id):
#         my_user_model = get_user_model()
#         try:
#             return my_user_model.objects.get(pk=user_id)
#         except my_user_model.DoesNotExist:
#             return None

    #
    # def authenticate(self, username=None, password=None):
    #     cu = CustomUser.objects.get(pk=1)
    #     print(1)
    #     return cu
    #
    # def get_user(self, user_id):
    #     print(2)
    #     cu = CustomUser.objects.get(pk=1)
    #     return cu