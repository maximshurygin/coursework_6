# Generated by Django 4.2.5 on 2023-10-03 12:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('service', '0013_newsletter_is_active_alter_newsletter_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'permissions': [('can_toggle_active', 'Can toggle active status')], 'verbose_name': 'Рассылка',
                     'verbose_name_plural': 'Рассылки'},
        ),
    ]
