# Generated by Django 4.1.4 on 2023-02-22 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0018_rename_period_meterpoint_period_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestmedia',
            name='request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_media', to='property.request'),
        ),
    ]
