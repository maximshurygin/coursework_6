# Generated by Django 4.2.5 on 2023-09-17 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_rename_newslettersettings_newsletter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
