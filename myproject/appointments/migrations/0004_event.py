# Generated by Django 5.1.3 on 2024-11-21 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_consultationrequest_appointment_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
    ]
