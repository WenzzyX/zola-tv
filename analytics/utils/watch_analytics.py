from analytics.utils.user_info import get_user_info
from analytics.models import BannerAnalytics, EventAnalytics, FirstAnalytics
from django.contrib.contenttypes.models import ContentType
from main.models import AdVideoBanner, Adbanner, AdVideoMidroll
from random import randint

def add_view(model):
    model.watch_counter = model.watch_counter + 1
    model.save()
    return True

# def get_banner(id, model):
#     model_type = ContentType.objects.get_for_model(model)



def save_event(request):
    event = request.POST.get('event')
    pev = request.POST.get('pev')
    url = request.POST.get('url')
    user_info = get_user_info(request.META)
    if pev == 'true':
        allowed_events = ['d_app', 'cr_prof']
        if event in allowed_events:
            event = EventAnalytics(
                type=event,
                url=url,
                user_agent=user_info['user_agent'],
                accept_language=user_info['accept_language'],
                ip=user_info['ip'],
                country=user_info['country'],
                datetime=user_info['time']
            )
            event.save()
            return 'OK'

    id = request.POST.get('addit_info')

    if id is not None:
        if event == 'cl_vid_b' or event == 'sh_vid_b':
            # content_obj = get_banner(id, AdVideoBanner)
            content_obj = AdVideoBanner.objects.get(id=id)
        elif event == 'cl_b':
            # content_obj = get_banner(id, Adbanner)
            content_obj = Adbanner.objects.get(id=id)

        elif event == 'cl_vid_midroll_b':
            content_obj = AdVideoMidroll.objects.get(id=id)
        else:
            return "OK"

    try:
        event = BannerAnalytics(
            type=event,
            url=url,
            user_agent=user_info['user_agent'],
            accept_language=user_info['accept_language'],
            ip=user_info['ip'],
            country=user_info['country'],
            datetime=user_info['time'],
            content_object=content_obj
        )
        event.save()
    except:
        pass
    return 'OK'

def save_first(request):
    url = request.POST.get('url')
    uid = randint(1000000, 99999999)
    a_id = request.POST.get('ad_id')
    user_info = get_user_info(request.META)
    try:
        event = FirstAnalytics(
            u_id=uid,
            a_id=a_id,
            url=url,
            user_agent=user_info['user_agent'],
            accept_language=user_info['accept_language'],
            ip=user_info['ip'],
            country=user_info['country'],
            datetime=user_info['time']
        )
        event.save()
        return uid
    except:
        return 'Error'
