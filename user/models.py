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

