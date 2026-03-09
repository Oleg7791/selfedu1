from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

from .models import Category, Husband

@deconstructible
class RussianValidator:
    """создаем класс для собственного валидатора
        который можем использовать как в форме, так и в модели
        нужно добавить в форму(например title),
        удобен для много кратного использования для разных полей"""
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            from django.core.exceptions import ValidationError
            raise ValidationError(self.message, code=self.code, params={"value": value})

class AddPostForm(forms.Form):
    """класс для создания формы(html) не связанной с моделью"""
    # используем названия атрибутов как в модели чтоб не запутаться
    title = forms.CharField(max_length=255,
                            min_length=5,
                            # validators=[
                            #     RussianValidator(),
                            # ],
                            error_messages={
                                'min_length':"Слишком короткий заголовок",
                                'required': "Без заголовка никак"
                            },
                            label='Заголовок')
    slug = forms.SlugField(max_length=255, label='URL',
                           validators=[
                               MinLengthValidator(5,message='Минимум 5 символов'),#через message= можно прописать своё сообщение
                               MaxLengthValidator(100)
                           ])
    content = forms.CharField(widget=forms.Textarea(), required=False, label='Контент')# required=False делает поле не обязательным для заполнения
    is_published = forms.BooleanField(required=False, label='Статус')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label='Категория не выбрана', label='Категории')# queryset=Category в форме будет
    # отображаться выпадающий список из категорий
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False,empty_label='Не замужем', label='Муж')

    def clean_title(self):
        """создания метода валидатора, где (clean_title) title атрибут
         для которого создаем валидатор,
         удобен для частного случая например одного поля"""
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские символы, дефис и пробел.")
        return title
