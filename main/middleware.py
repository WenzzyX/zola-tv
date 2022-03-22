# class CORSMiddleware(object):
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         response["Access-Control-Allow-Origin"] = "*"
#
#         return response


import time
from django.http import HttpResponseRedirect
from django.conf import settings
import re


def timing(get_response):
    def middleware(request):
        req_path = request.path
        req_lang = settings.LANGUAGE_CODE if request.COOKIES == {} else request.LANGUAGE_CODE

        query_str = request.META['QUERY_STRING']
        req_gets = ''
        if query_str:
            req_gets = f'?{query_str}'
        response = get_response(request)
        matched = False
        for path in settings.NO_REDIRECT_PATHS:
            if re.search(path, req_path):
                matched = True
        if matched:
            return response
        # print('PATH : ', req_path)
        match_qu = f'/{req_lang}/'
        # print(match_qu)
        try:
            # print('RQUE : ', re.search(match_qu, req_path))
            if not re.search(match_qu, req_path):
                return HttpResponseRedirect(f'/{req_lang}{req_path}{req_gets}')

        except:
            pass
        return response

    return middleware
