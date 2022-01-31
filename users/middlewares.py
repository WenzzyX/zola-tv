from django.contrib.auth import get_user_model
from ipware import get_client_ip
UserModel = get_user_model()


class IpHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        # print(1)
        # self.process_request()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # print(1)
        response = self.get_response(request)
        self.process_request(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        USER_IP = get_client_ip(request)
        if request.user.is_authenticated:
            UserModel.objects.filter(id=request.user.id).update(last_login_ip=USER_IP[0])

# class LastLoginIP(object):
