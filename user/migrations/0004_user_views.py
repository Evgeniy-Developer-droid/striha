# Generated by Django 4.1.4 on 2023-02-24 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
