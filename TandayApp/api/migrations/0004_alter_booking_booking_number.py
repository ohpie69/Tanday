# Generated by Django 5.1.1 on 2024-11-11 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_booking_booking_number_booking_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_number',
            field=models.CharField(default='80FEF3DCFDC9', editable=False, max_length=12),
        ),
    ]
