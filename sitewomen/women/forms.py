from django import forms
from .models import Category, Husband

class AddPostForm(forms.Form):
    """класс для создания формы(html) не связанной с моделью"""
    # используем названия атрибутов как в модели чтоб не запутаться
    title = forms.CharField(max_length=255, label='Заголовок')
    slug = forms.SlugField(max_length=255, label='URL')
    content = forms.CharField(widget=forms.Textarea(), required=False, label='Контент')# required=False делает поле не обязательным для заполнения
    is_published = forms.BooleanField(required=False, label='Статус')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label='Категория не выбрана', label='Категории')# queryset=Category в форме будет
    # отображаться выпадающий список из категорий
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False,empty_label='Не замужем', label='Муж')