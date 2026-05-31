from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import CharField
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name='Slug')
    # поле атрибут для загрузки фотографий 'photo', не забываем выполнять
    # миграции после изменения модели
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None,
                              blank=True, null=True, verbose_name='Фото')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True,verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                                     default=Status.DRAFT, verbose_name='Статус')
    # создаем атрибут для связывания моделей Many to one(пост и категории)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name='posts',
                            verbose_name='Категория')
    # создаем атрибут для связи Many to Many
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags',
                                  verbose_name='Теги')
    # создаем атрибут для связи One to One (будет связывать женщин с их мужьями
    # параметр on_delete=models.SET_NULL отвечает если удалить мужа то значение примет Null,
    # blank=True - позволяет поле оставлять пустым, related_name='wuman'- атрибут для обратного связывания
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='wuman',
                                   verbose_name='Муж')
    # поле автор для указания в посте автора
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='posts', null=True, default=None)

    objects = models.Manager() # стандартный менеджер
    published = PublishedManager()  # создание нового менеджера

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Известные женщины"  # Редактируем меняем название в админ панели
        verbose_name_plural = "Известные женщины"  # тоже, но чтобы и во множественном числе
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

class UploadFiles(models.Model):
    """создаем модель для загрузки файлов"""
    file = models.FileField(upload_to='uploads_model')# параметр "uploads_model" создает
    # папку с выбранным параметром, не забываем применить миграцию


User = get_user_model()


class Profile(models.Model):
    """Расширение модели User через One-to-One связь"""

    # Связь один-к-одному с моделью User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',  # Для доступа user.profile
        verbose_name='Пользователь'
    )

    # Дополнительные поля для расширения
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )

    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе'
    )

    # Социальные сети
    telegram = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Telegram'
    )

    github = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='GitHub'
    )

    # Служебные поля
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-created_at']

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    def get_full_info(self):
        """Метод для получения полной информации о пользователе"""
        info = {
            'username': self.user.username,
            'email': self.user.email,
            'phone': self.phone,
            'birth_date': self.birth_date,
            'bio': self.bio,
        }
        return info


# Сигналы для автоматического создания профиля при регистрации
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создает профиль при создании нового пользователя"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при сохранении пользователя"""
    # Проверяем, есть ли профиль, если нет - создаем
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()