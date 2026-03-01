from django.contrib import admin, messages
from django.db.models.functions import Length
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
    fields = ['title', 'slug', 'content', 'cat','husband','tags']  # атрибут список полей которые отображаются в форме редактирования
    #readonly_fields = ['slug']# атрибут позволяющий сделать отображаемое поле не редактируемым
    prepopulated_fields = {'slug':('title',)}# атрибут используется для автоматического
    # заполнения поля слага, но должен быть не активен атрибут 'readonly_fields'
    filter_horizontal = ['tags']# атрибут добавляет виджет в виде табличек удобность
    list_display = ('id', 'title', 'time_create', 'is_published', "cat", "brief_info")  # список отображаемых полей
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

    # появился в панели фильтров MarriedFilter

    @admin.display(description="Краткое описание",
                   ordering=Length('content'))  # класс Length позволяет сортировать по кол-ву символов
    def brief_info(self, women: Women):
        """метод создает поле (в списке статей) админке, ее не будет в базе данных,
        добавим в list_display"""
        return f"Описание {len(women.content)} символов"

    @admin.action(description="Опубликовать выбранные записи")  # декоратор для перевода записи
    def set_published(self, request, queryset):
        """ будем для выбора записей в разряд опубликованные"""
        count = queryset.update(is_published=Women.Status.PUBLISHED)  # count добавлен счетчик измененных записей
        self.message_user(request, f"Изменено {count} записей.", messages.SUCCESS)

    @admin.action(description="Снять с публикации выбранные записи")  # декоратор для перевода записи
    def set_draft(self, request, queryset):
        """ будем для выбора записей в разряд снятые с публикации"""
        count = queryset.update(is_published=Women.Status.DRAFT)  # count добавлен счетчик измененных записей
        self.message_user(request, f"{count} записей снято с публикации!", messages.WARNING)


# admin.site.register(Women, WomenAdmin) # добавили в декоратор

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ класс для настройки отображения Модели -Категории в админ панели"""
    list_display = ('id', 'name')  # список отображаемых полей
    list_display_links = ('id', 'name')  # атрибут делает активными поля в админке
