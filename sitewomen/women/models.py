from django.db import models

class PublishedManager(models.Manager):
    """класс создающий пользовательский менеджер, который будет
    возвращать только опубликованные посты"""
    def get_queryset(self):
        """метод возвращает все запросы с помощью get_queryset из
         базового класса применяя фильтр, только опубликованные"""
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):

    class Status(models.IntegerChoices):
        """спец класс для определения статуса опубликован или нет"""
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликованный'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManager() # создание нового менеджера

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]