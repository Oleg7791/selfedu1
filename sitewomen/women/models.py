from django.db import models
from django.urls import reverse

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
    # создаем атрибут для связывания моделей Many to one(пост и категории)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name='posts')
    # создаем атрибут для связи Many to Many
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    objects = models.Manager()
    published = PublishedManager() # создание нового менеджера

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        """функция помогает выводить полностью посты,
         прописываем в index.html обязательно импортируем """
        return reverse('post', kwargs={'post_slug':self.slug})

class Category(models.Model):
    """Определяем модель для категорий"""

    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        """в случае обращения к Категории будет выводить ИМя(name)"""
        return self.name

    def get_absolute_url(self):
        """специальный метод формирует полноценный урл адрес,
        который будет подставляться в list_categories.html"""
        return reverse('category',kwargs={'cat_slug':self.slug})

class TagPost(models.Model):
    """класс для создания Модели для тэгов"""
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        """нужен для того когда будем отображать запись
        модели TagPost будут отображаться названия тэгов (tag)"""
        return self.tag

    def get_absolute_url(self):
        """специальный метод формирует полноценный урл адрес,
        который будет возвращать тот или иной адрес для конкретного тэга"""
        return reverse('tag',kwargs={'tag_slug':self.slug})

