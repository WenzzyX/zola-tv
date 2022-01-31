from geoip import geolite2
from django.utils.timezone import now

def get_user_info(meta):
    x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        uip = x_forwarded_for.split(',')[0]
    else:
        uip = meta.get('REMOTE_ADDR')

    ipinfo = geolite2.lookup(uip)
    u_country = 'None'
    if ipinfo is not None:
         u_country = ipinfo.country
    dict_userinfo = {
        "user_agent": meta['HTTP_USER_AGENT'],
        "accept_language": meta['HTTP_ACCEPT_LANGUAGE'],
        "ip": meta['REMOTE_ADDR'],
        "country": u_country,
        "time": now()
    }
    return dict_userinfo
