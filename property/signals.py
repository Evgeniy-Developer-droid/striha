from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from property.models import Contract


@receiver(post_save, sender=Contract)
def contract_post_save_signals(sender, instance, created, **kwargs):
    if instance.status == "active":
        instance.real_estate.status = "rented"
        instance.real_estate.save()

    if instance.status == "terminated":
        instance.real_estate.status = "not_rented"
        instance.real_estate.save()

        
