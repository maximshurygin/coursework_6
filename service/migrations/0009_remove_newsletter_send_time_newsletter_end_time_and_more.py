# Generated by Django 4.2.5 on 2023-09-17 15:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('service', '0008_alter_message_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='send_time',
        ),
        migrations.AddField(
            model_name='newsletter',
            name='end_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время окончания'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='start_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время начала'),
        ),
    ]
