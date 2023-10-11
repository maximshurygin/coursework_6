from django.db import models
from django.utils import timezone


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog_images/', verbose_name='Изображение', blank=True, null=True)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    publication_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
