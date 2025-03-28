# Generated by Django 5.1.5 on 2025-01-25 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_event_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phonenumber', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('pincode', models.CharField(max_length=10)),
                ('preferable_date', models.DateField()),
                ('preferred_location', models.CharField(choices=[('City Center', 'City Center'), ('Beach Side', 'Beach Side'), ('Garden Venue', 'Garden Venue'), ('Indoor Hall', 'Indoor Hall')], max_length=100)),
                ('event_ideas', models.TextField(blank=True, null=True)),
                ('food_preferences', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
