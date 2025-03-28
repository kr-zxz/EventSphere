# Generated by Django 5.1.5 on 2025-02-20 04:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_alter_booking_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='sentiment',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
    ]
