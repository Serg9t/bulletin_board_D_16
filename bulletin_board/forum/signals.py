from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Response


# Отправлять уведомление пользователю, если его отклик был принят
@receiver(post_save, sender=Response)
def confirm_response(sender, instance, **kwargs):
    if instance.status:
        email = instance.author.email

        send_mail(
            subject='Оповещение',
            message='Ваш отклик приняли!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
