from django.template.loader import render_to_string
from django.core.signing import Signer
from MyForum.settings import ALLOWED_HOSTS
from os.path import splitext
import datetime


def available_birth_years(min_year=1900):
    return [f'{year}' for year in range(min_year, datetime.datetime.now().year + 1)]


def get_timestamp_path(instance, filename):
    return f'{datetime.datetime.now().timestamp()}{splitext(filename)[1]}'


signer = Signer()


def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {
        'user': user,
        'host': host,
        'sign': signer.sign(user.username)  # Создание уникальной цифровой подписи пользователя
    }
    subject = render_to_string(
        template_name='email/activation_letter_subject',
        context=context,
    )
    body_text = render_to_string(
        template_name='email/activation_letter_body',
        context=context,
    )
    user.email_user(subject, body_text)
