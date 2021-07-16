from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import mail_managers, mail_admins, send_mail
from .models import *


@receiver(post_save, sender=Post)
def sub_mail(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.preview_name} {instance.dateCreation.strftime("%d %m %Y")}'
    else:
        subject = f'Изменено  {instance.preview_name} {instance.dateCreation.strftime("%d %m %Y")}'

    send_mail(
        subject=subject,
        message=instance.text,
        from_email='skillf.trofimova@yandex.ru',
        recipient_list=['kateno4egg@gmail.com']
    )


@receiver(post_delete, sender=Post)
def sub_mail_del(sender, instance, **kwargs):
    subject = f'{instance.preview_name} удалено!'
    send_mail(
        subject=subject,
        message=f'Удалено {instance.dateCreation.strftime("%d %m %Y")}',
        from_email='skillf.trofimova@yandex.ru',
        recipient_list=['kateno4egg@gmail.com']
    )