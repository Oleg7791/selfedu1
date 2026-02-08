from django.urls import reverse
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
    # добавляем атрибут для связи первичного класса Category с вторичным классом Women
    cat = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='posts')

    objects = models.Manager()  # стандартный менеджер записи
    published = PublishedManager() # создание нового менеджера

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

class Category(models.Model):
    """Определяем ещё одну модель для категорий"""
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    def __str__(self):
        """нужен чтобы при выводе мы видели понятную информацию
        в нашем случае будем возвращать название категории"""
        return self.name

    def get_absolute_url(self):
        """формирует полноценный урл адрес в list_categories.html,
        пришлось импортировать from django.urls import reverse"""
        return reverse('category',kwargs={'cat_slug':self.slug})