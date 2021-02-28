from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
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


def set_host():
    if ALLOWED_HOSTS:
        return 'http://' + ALLOWED_HOSTS[0]
    else:
        return 'http://localhost:8000'


def send_activation_notification(user):
    context = {
        'user': user,
        'host': set_host(),
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


def send_confirmation_to_update_personal_information(user):
    context = {
        'user': user,
        'host': set_host(),
        'sign': signer.sign(user.username),
    }

    subject = render_to_string(
        template_name='email/change_personal_info_subject',
        context=context
    )
    body_text = render_to_string(
        template_name='email/change_personal_info_body',
        context=context
    )
    user.email_user(subject=subject, message=body_text)


def send_request_to_change_password(user):
    token = PasswordResetTokenGenerator()
    context = {
        'user': user,
        'host': set_host(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token.make_token(user=user),
    }

    subject = render_to_string(
        template_name='email/user_forgot_password_subject',
        context=context
    )
    body_text = render_to_string(
        template_name='email/user_forgot_password_body',
        context=context
    )
    user.email_user(subject=subject, message=body_text)
