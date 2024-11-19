# Generated by Django 5.1.1 on 2024-11-11 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_booking_booking_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_number',
            field=models.CharField(default='A8FF04A95E91', editable=False, max_length=12),
        ),
        migrations.AlterField(
            model_name='booking',
            name='check_in',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='check_out',
            field=models.DateField(blank=True, null=True),
        ),
    ]