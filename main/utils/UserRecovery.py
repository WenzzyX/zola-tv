from users.models import CodeRecovery
from sms import send_sms
from django.conf import settings
from users.userActivation import get_random_code
from django.core.mail import send_mail
from django.utils.timezone import now

def check_recovery_sended(user):
    try:
        rec = CodeRecovery.objects.get(user=user)
        print(2)
        return True
    except CodeRecovery.DoesNotExist:
        print(3)
        return False


def check_code(user, code):
    ucode = CodeRecovery.objects.get(user=user)
    if ucode.code == code:
        return True
    return False


def _send_mail(to, message):
    emails = []
    emails.append(to)
    send_mail('ZolaTV | Password recovery', message, 'best.cinema.app@gmail.com', emails, fail_silently=True)

def _send_sms(to, message):
    phones = []
    phones.append(to)
    send_sms(
        body=message,
        originator=settings.TWILIO_PHONE_NUMBER,
        recipients=phones,
        fail_silently=True
    )

def send_code(user, type):
    generated_code = get_random_code()
    code = CodeRecovery(
        user=user,
        code=generated_code
    )
    if type == 'email':
        code.is_email = True
        print('EMAIL')
        _send_mail(to=user.email, message=f"You're code for recovery password on ZolaTV is: {generated_code}")
    elif type == 'phone':
        print('PHONE')
        _send_sms(to=f'+{user.phone}',
                      message=f"You're code for recovery password on ZolaTV is: {generated_code}")
    code.save()

def delete_code(user):
    CodeRecovery.objects.get(user=user).delete()
    return True

def check_seconds(user):
    time_send = CodeRecovery.objects.get(user=user).time
    current_time = now()
    if (current_time - time_send).seconds > 60:
        return True
    else:
        return False