from django.conf import settings
from django.db import models


# Create your models here.


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Контактный Email")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(blank=True, null=True,
                               verbose_name="Комментарий")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name="Владелец", blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Текст письма")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name="Владелец", blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Newsletter(models.Model):
    PERIODICITY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )
    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    )
    recipients = models.ManyToManyField(Client,
                                        verbose_name="Получатели рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE,
                                verbose_name="Сообщение рассылки",
                                null=True, blank=True)
    start_time = models.TimeField(verbose_name="Время начала", null=True,
                                  blank=True)
    end_time = models.TimeField(verbose_name="Время окончания", null=True,
                                blank=True)
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES,
                                   verbose_name="Периодичность")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              verbose_name="Статус рассылки")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name="Владелец", blank=True, null=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f"Рассылка {self.get_periodicity_display()} " \
               f"в {self.start_time} - {self.end_time}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ("can_toggle_active", "Can toggle active status"),
        ]


class Log(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE,
                                   verbose_name="Рассылка")
    attempt_datetime = models.DateTimeField(auto_now_add=True,
                                            verbose_name="Дата и время "
                                                         "последней попытки")
    status = models.BooleanField(default=True, verbose_name="Статус")
    server_response = models.TextField(blank=True, null=True,
                                       verbose_name="Ответ почтового сервера")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name="Владелец", blank=True, null=True)

    def __str__(self):
        status = 'Успешно' if self.status else 'Неуспешно'
        return f"Лог рассылки для {self.newsletter} - {status}"

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
