from django.db import models

from authentification.utils import generate_token


class AuthToken(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, default=generate_token, blank=True)
    name = models.CharField(max_length=255, default="", blank=True)
    meta = models.CharField(max_length=255, default="", blank=True)
