from django.contrib import admin

from .models import Women, Category


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    """ класс для настройки отображения статей в админ панели Модель-Women"""
    list_display = ('id', 'title', 'time_create', 'is_published',"cat")  # список отображаемых полей
    list_display_links = ('id', 'title')# атрибут делает активными поля в админке
    ordering = ['time_create','title'] # атрибут список полей по которым сортируем
    list_editable = ('is_published',)# атрибут определяющий список(кортеж) полей которые можно
    # редактировать, нужно прописать костыль для статуса " (choices=tuple(map(lambda x: (bool(x[0]), x[1]), "
    # для преобразования в булевы значения
    list_per_page = 3 #атрибут устанавливающий количество статей на одной странице

# admin.site.register(Women, WomenAdmin) # добавили в декоратор

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ класс для настройки отображения Модели -Категории в админ панели"""
    list_display = ('id', 'name')  # список отображаемых полей
    list_display_links = ('id', 'name')# атрибут делает активными поля в админке
