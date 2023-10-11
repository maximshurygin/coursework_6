# Generated by Django 4.2.5 on 2023-10-03 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0011_client_owner_log_owner_message_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('created', 'Создана'), ('running', 'Запущена'), ('completed', 'Завершена'), ('deactivated', 'Отключена')], max_length=20, verbose_name='Статус рассылки'),
        ),
    ]