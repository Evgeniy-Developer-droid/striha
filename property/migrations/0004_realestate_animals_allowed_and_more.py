# Generated by Django 4.1.4 on 2022-12-25 21:21

import authentification.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0003_rename_propertymedia_realestatemedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='realestate',
            name='animals_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='realestate',
            name='children_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='realestate',
            name='floor',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AddField(
            model_name='realestate',
            name='landlord',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='real_estate_landlord', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='realestate',
            name='price_month',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='realestate',
            name='rooms',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AddField(
            model_name='realestate',
            name='share_token',
            field=models.CharField(blank=True, default=authentification.utils.generate_token, max_length=255),
        ),
        migrations.AddField(
            model_name='realestate',
            name='smokers_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='realestate',
            name='status',
            field=models.CharField(blank=True, choices=[('not_rented', 'Not rented'), ('disable', 'Disable'), ('rented', 'Rented')], default='not_rented', max_length=255),
        ),
        migrations.AddField(
            model_name='realestate',
            name='students_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='realestate',
            name='tenants',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AddField(
            model_name='realestate',
            name='type_real_estate',
            field=models.CharField(blank=True, choices=[('house', 'House'), ('appartment', 'Appartment'), ('single_room', 'Single rooom')], default='house', max_length=255),
        ),
    ]
