from django.db import models
from django.db.models.fields import CharField
from django.template.defaultfilters import slugify
from django.urls import reverse

def translit_to_eng(s: str):
    """специальная функция Костыль для преобразования латиницы в кириллицу
    используется для вывода автоматом слага"""
    d = {
        'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ж':'zh', 'з':'z', 'и':'i',
        'к':'k', 'л':'l', 'м':'m', 'н':'n', 'о':'o', 'п':'p', 'р':'r', 'с':'s', 'т':'t',
        'у':'u', 'ф':'f', 'х':'h', 'ц':'c', 'ч':'ch','ш':'sch', 'щ':'schc', 'ы':'y', 'э':'r',
        'ю':'yu', 'я':'ya'
    }
    return ''.join(map(lambda x: d[x] if d.get(x,False) else x, s.lower()))

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

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True,verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                                     default=Status.DRAFT, verbose_name='Статус')
    # создаем атрибут для связывания моделей Many to one(пост и категории)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name='posts',verbose_name='Категория')
    # создаем атрибут для связи Many to Many
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    # создаем атрибут для связи One to One (будет связывать женщин с их мужьями
    # параметр on_delete=models.SET_NULL отвечает если удалить мужа то значение примет Null,
    # blank=True - позволяет поле оставлять пустым, related_name='wuman'- атрибут для обратного связывания
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='wuman', verbose_name='Муж')

    objects = models.Manager() # стандартный менеджер
    published = PublishedManager()  # создание нового менеджера

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Известные женщины"  # Редактируем меняем название в админ панели
        verbose_name_plural = "Известные женщины"  # тоже но чтобы и во множественном числе
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        """функция помогает выводить полностью посты,
         прописываем в index.html обязательно импортируем """
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self,*args,**kwargs):
    #     """спец метод для сохранения слага по набору заголовка"""
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)


class Category(models.Model):
    """Определяем модель для категорий"""

    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        """в случае обращения к Категории будет выводить ИМя(name)"""
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        """специальный метод формирует полноценный урл адрес,
        который будет подставляться в list_categories.html"""
        return reverse('category', kwargs={'cat_slug': self.slug})


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
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    """создаем модель МУЖ на ней будем изучать связь One to One"""
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        """метод будет возвращать имя name при обращении к модели"""
        return self.name
