# Generated by Django 5.1.2 on 2024-11-27 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_booking_booking_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_number',
            field=models.CharField(default='AD1CED7152B4', editable=False, max_length=12),
        ),
    ]
