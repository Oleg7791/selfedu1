from django import forms
from .models import Category, Husband

class AddPostForm(forms.Form):
    """класс для создания формы(html) не связанной с моделью"""
    # используем названия атрибутов как в модели чтоб не запутаться
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False)# required=False делает поле не обязательным для заполнения
    is_published = forms.BooleanField(required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())# queryset=Category в форме будет
    # отображаться выпадающий список из категорий
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False)