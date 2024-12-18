# Generated by Django 5.1.3 on 2024-11-20 20:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_consultationrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationrequest',
            name='appointment_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultationrequest',
            name='appointment_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
