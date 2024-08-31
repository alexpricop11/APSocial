import random
import string
from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response


def send_password_reset_email(to_email, reset_code):
    subject = 'Resetare Parola'
    message = f'Pentru a reseta parola, folosește codul: {reset_code}'
    from_email = 'APSocial <apricop05@gmail.com>'
    send_mail(subject, message, from_email, [to_email])


def get_user_email(user):
    email = user.email
    if not email:
        return Response({'error': 'This user has no email'})
    reset_code = ''.join(random.choices(string.digits, k=4))
    expiry_time = timezone.now() + timedelta(hours=1)
    user.reset_code = reset_code
    user.reset_code_expiry = expiry_time
    user.save()
    send_password_reset_email(email, reset_code)


def password_reset(user, reset_code, new_password):
    if user.reset_code == reset_code and timezone.now() <= user.reset_code_expiry:
        if user.check_password(new_password):
            return Response('New password cannot be the same as the old password',
                            status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.reset_code = None
        user.reset_code_expiry = None
        user.save()
    return Response({'error': 'Invalid or expired reset code'}, status=status.HTTP_400_BAD_REQUEST)
