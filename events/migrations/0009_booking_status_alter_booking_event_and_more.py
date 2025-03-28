# Generated by Django 5.1.5 on 2025-01-27 08:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_booking_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Cancelled', 'Cancelled'), ('Waiting', 'Waiting')], default='Waiting', max_length=20),
        ),
        migrations.AlterField(
            model_name='booking',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='event_type',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='booking',
            name='location_details',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='payment_method',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='pincode',
            field=models.CharField(max_length=6),
        ),
    ]
