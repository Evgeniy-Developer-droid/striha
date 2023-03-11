import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE = (
        ('tenant', 'Tenant',),
        ('landlord', 'Landlord',),
    )
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=255, default="", null=True, blank=True)
    role = models.CharField(max_length=255, choices=ROLE, default='tenant')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    views = models.IntegerField(default=0)


class SocialLink(models.Model):
    name = models.CharField(max_length=255, default="", null=True, blank=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    url = models.CharField(max_length=500, default="", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class UserReview(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_user_review")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target_user_review")
    body = models.TextField(default="", blank=True)


class Notification(models.Model):
    META_NAME = (
        ("request", "Request",),
        ("contract", "Contract",),
        ("payment", "Payment",),
        ("meterpoint", "Meterpoint",),
        ("other", "Other",),
    )
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    viewed = models.BooleanField(default=False)
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target_user_notification")
    title = models.CharField(max_length=500, default="", null=True, blank=True)
    body = models.CharField(max_length=500, default="", null=True, blank=True)
    meta_name = models.CharField(max_length=500, choices=META_NAME, default="other")


class P2PCredit(models.Model):
    STATUS = (
        ('pending', "Pending",),
        ('success', "Success",),
        ('failure', "Failure",),
        ('error', "Error",),
    )
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.IntegerField(default=0)
    currency = models.CharField(max_length=10, default="UAN")
    order_id = models.CharField(max_length=255, default="")
    card = models.CharField(max_length=255, default="**** **** **** 0000")
    status = models.CharField(max_length=255, choices=STATUS, default="pending")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="p2p_credit_user")

    payment_id = models.CharField(max_length=255, default="unknown")
    acq_id = models.CharField(max_length=255, default="unknown")
    liqpay_order_id = models.CharField(max_length=255, default="unknown")
    transaction_id = models.CharField(max_length=255, default="unknown")

    meta = models.TextField(default="{}", blank=True)

    description = models.TextField(default="", blank=True)
    # https://www.liqpay.ua/documentation/api/p2p_credit/doc