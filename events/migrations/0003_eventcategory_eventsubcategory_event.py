# Generated by Django 5.1.4 on 2025-01-17 07:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_userprofile_profile_image_alter_userprofile_age_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/')),
            ],
        ),
        migrations.CreateModel(
            name='EventSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='events.eventcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='events/')),
                ('location', models.CharField(choices=[('Indoor', 'Indoor'), ('Outdoor', 'Outdoor')], max_length=200)),
                ('date', models.DateField()),
                ('package_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.eventcategory')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.eventsubcategory')),
            ],
        ),
    ]
