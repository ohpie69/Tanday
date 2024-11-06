import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import uuid

def generate_unique_booking_numbers(apps, schema_editor):
    Booking = apps.get_model('api', 'Booking')
    for booking in Booking.objects.all():
        booking.booking_number = uuid.uuid4().hex[:12].upper()  # Generate a unique 12-character UUID
        booking.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_booking_room_type_booking_room_types_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_number',
            field=models.CharField(max_length=12, unique=True, editable=False, null=True),
        ),
        migrations.RunPython(generate_unique_booking_numbers),  # Populate each record with a unique value
        migrations.AlterField(
            model_name='booking',
            name='booking_number',
            field=models.CharField(max_length=12, unique=True, editable=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
