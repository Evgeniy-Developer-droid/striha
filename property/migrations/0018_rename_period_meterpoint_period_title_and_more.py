# Generated by Django 4.1.4 on 2023-02-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0017_alter_transaction_mode_meterpoint'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meterpoint',
            old_name='period',
            new_name='period_title',
        ),
        migrations.AddField(
            model_name='meterpoint',
            name='period_month',
            field=models.CharField(choices=[('january', 'January'), ('february', 'February'), ('march', 'March'), ('april', 'April'), ('may', 'May'), ('june', 'June'), ('july', 'July'), ('august', 'August'), ('september', 'September'), ('october', 'October'), ('november', 'November'), ('december', 'December')], default='', max_length=255),
        ),
        migrations.AddField(
            model_name='meterpoint',
            name='period_year',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='liqpay_order_id',
            field=models.CharField(blank='', default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_id',
            field=models.CharField(blank='', default='', max_length=255),
        ),
    ]
