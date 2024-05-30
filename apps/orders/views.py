from django.shortcuts import render


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from apps.orders.models import Order
from apps.users.models import User


@receiver(post_save, sender=Order)
def notify_status_change(sender, instance, **kwargs):
    if instance.status == 'Ready':
        waiter_email = instance.waiter.email
        send_mail(
            'Order Ready Notification',
            f'Order {instance.id} for Table {instance.table.number} is ready.',
            'from@example.com',
            [waiter_email],
            fail_silently=False,
        )
    elif instance.status == 'Closed':
        cashiers = User.objects.filter(user_type='box')
        cashier_emails = [cashier.email for cashier in cashiers]
        send_mail(
            'Table Payment Notification',
            f'Table {instance.table.number} is ready for payment.',
            'from@example.com',
            cashier_emails,
            fail_silently=False,
        )
