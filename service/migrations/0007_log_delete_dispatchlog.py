# Generated by Django 4.2.5 on 2023-09-17 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('service', '0006_alter_dispatchlog_newsletter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_datetime',
                 models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')),
                ('status', models.BooleanField(default='Успешно', verbose_name='Статус')),
                ('server_response', models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
                ('newsletter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.newsletter',
                                                 verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
        migrations.DeleteModel(
            name='DispatchLog',
        ),
    ]
