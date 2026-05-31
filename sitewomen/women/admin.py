from django.contrib import admin, messages
from django.db.models.functions import Length
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Profile


from .models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    """добавляет свой самими созданный фильтр в панель фильтрации"""
    title = "Статус женщин"  # атрибут определяющий название фильтра
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """метод возвращает список из возможных параметров parameter_name = 'status' """
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]

    def queryset(self, request, queryset):
        """возвращает набор записей для фильтра"""
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
# admin.site.register(Women, WomenAdmin) # добавили в декоратор
class WomenAdmin(admin.ModelAdmin):
    """ класс для настройки отображения статей в админ панели Модель-Women"""
    fields = ['title', 'slug', 'content', 'photo','post_photo', 'cat','husband','tags']  # атрибут список полей которые отображаются в форме редактирования
    #readonly_fields = ['slug']# атрибут позволяющий сделать отображаемое поле не редактируемым
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug':('title',)}# атрибут используется для автоматического
    # заполнения поля слага, но должен быть не активен атрибут 'readonly_fields'
    filter_horizontal = ['tags']# атрибут добавляет виджет в виде табличек удобность
    list_display = ('id', 'title', 'post_photo', 'time_create', 'is_published', "cat", "brief_info")  # список отображаемых полей
    list_display_links = ('id', 'title')  # атрибут делает активными поля в админке
    ordering = ['time_create', 'title']  # атрибут список полей по которым сортируем
    list_editable = ('is_published',)  # атрибут определяющий список(кортеж) полей которые можно
    # редактировать, нужно прописать костыль для статуса " (choices=tuple(map(lambda x: (bool(x[0]), x[1]), "
    # для преобразования в булевы значения
    list_per_page = 4  # атрибут устанавливающий количество статей на одной странице
    # спец атрибут для вывода надписи в админки (в выпадающей панельке "действие" для группового выбора
    actions = ['set_published', 'set_draft']
    # создаем атрибут, который добавляет новую панель поиска
    search_fields = ['title', "cat__name"]
    """чтобы прописать поля из связанной таблицы используем двойное подчеркивание cat__name"""
    # атрибут для создания панели фильтрации
    list_filter = [MarriedFilter, 'cat__name', 'is_published']  # прописываем название класса чтобы
    save_on_top = True # атрибут добавляет сверху панельку сохранить и т.д.

    # появился в панели фильтров MarriedFilter

    @admin.display(description="Краткое описание",
                   ordering=Length('content'))  # класс Length позволяет сортировать по кол-ву символов
    def brief_info(self, women: Women):
        """метод создает поле (в списке статей) админке, ее не будет в базе данных,
        добавим в list_display"""
        return f"Описание {len(women.content)} символов"

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self,women:Women):
        """метод для отображения маленького фото """
        if women.photo:
            return mark_safe(f"<img  src = '{women.photo.url}' width=50>")# функция mark_safe нужна чтоб тег img не экранировал
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")  # декоратор для перевода записи
    def set_published(self, request, queryset):
        """ будем для выбора записей в разряд опубликованные"""
        count = queryset.update(is_published=Women.Status.PUBLISHED)  # count добавлен счетчик измененных записей
        self.message_user(request, f"Изменено {count} записей.", messages.SUCCESS)

    @admin.action(description="Снять с публикации выбранные записи")  # декоратор для перевода записи
    def set_draft(self, request, queryset):
        """ будем для выбора записей в разряд снятые с публикации"""
        count = queryset.update(is_published=Women.Status.DRAFT)  # count добавлен счетчик измененных записей
        self.message_user(request, f"{count} записей снято с публикации!",
                          messages.WARNING)


# admin.site.register(Women, WomenAdmin) # добавили в декоратор

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ класс для настройки отображения Модели -Категории в админ панели"""
    list_display = ('id', 'name')  # список отображаемых полей
    list_display_links = ('id', 'name')  # атрибут делает активными поля в админке


User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'

    # Поля профиля, которые будут отображаться
    fields = ('phone', 'birth_date', 'avatar', 'bio', 'telegram', 'github')

    # Если нужно сделать некоторые поля только для чтения
    readonly_fields = ('created_at', 'updated_at')


class CustomUserAdmin(BaseUserAdmin):
    """Расширяем стандартного UserAdmin"""

    # Встраиваем профиль
    inlines = [ProfileInline]

    # Поля в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_phone', 'is_staff', 'is_active')

    # Поля для поиска (включая поля профиля)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'profile__phone')

    # Фильтры
    list_filter = ('is_staff', 'is_active', 'date_joined')

    # Поля, доступные только для чтения
    readonly_fields = ('last_login', 'date_joined')

    # Метод для отображения телефона из профиля в списке
    def get_phone(self, obj):
        """Возвращает номер телефона из профиля"""
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.phone
        return '-'

    get_phone.short_description = 'Телефон'
    get_phone.admin_order_field = 'profile__phone'  # Для сортировки

    # Дополнительное поле для отображения на странице редактирования
    def profile_phone(self, obj):
        """Отображает телефон на странице редактирования"""
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.phone
        return '-'

    profile_phone.short_description = 'Телефон'

    # Добавляем профиль_фон в read only поля
    readonly_fields = BaseUserAdmin.readonly_fields + ('profile_phone',)

    # Организация полей на странице редактирования
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Информация из профиля', {
            'fields': ('profile_phone',),
            'classes': ('collapse',),
        }),
    )


# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Админка для модели Profile"""
    list_display = ('user', 'phone', 'birth_date', 'created_at')
    list_filter = ('created_at', 'birth_date')
    search_fields = ('user__username', 'user__email', 'phone')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Контактные данные', {
            'fields': ('phone', 'telegram', 'github')
        }),
        ('Личная информация', {
            'fields': ('birth_date', 'avatar', 'bio')
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )