# Generated by Django 4.1.4 on 2023-02-25 01:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('body', models.TextField(blank=True, default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_user_review', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_user_review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]