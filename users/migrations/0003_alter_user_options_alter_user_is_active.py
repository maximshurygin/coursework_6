# Generated by Django 4.2.5 on 2023-10-03 12:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('can_toggle_active', 'Can toggle active status')]},
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True,
                                      help_text='Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
