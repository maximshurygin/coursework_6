# Generated by Django 4.2.5 on 2023-09-17 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewsletterSettings',
            new_name='Newsletter',
        ),
    ]
