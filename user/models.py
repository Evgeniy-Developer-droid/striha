from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE = (
        ('tenant', 'Tenant',),
        ('landlord', 'Landlord',),
    )
    phone = models.CharField(max_length=255, default="", null=True, blank=True)
    role = models.CharField(max_length=255, choices=ROLE, default='tenant')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)


class SocalLink(models.Model):
    name = models.CharField(max_length=255, default="", null=True, blank=True)
    url = models.CharField(max_length=500, default="", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
