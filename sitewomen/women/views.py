from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .forms import AddPostForm
from .models import Women, Category, TagPost

menu = [
    {'title':'О сайте','url_name':'about'},
    {'title':"Добавить статью",'url_name':'add_page'},
    {'title':"Обратная связь",'url_name':'contact'},
    {'title':"Войти",'url_name':'login'}
]

def index(request):  # обязательный параметр request

    posts = Women.published.all().select_related('cat')# добавляем select_related('cat')
    # для использования "жадной" загрузки чтобы не было дублирующих запросов,
    # "cat" это атрибут связывающий ForeignKey в модели Women

    data = {
        'title': "Главная страница",
        'menu': menu,
        'posts': posts,
        "cat_selected": 0,

    }
    return render(request, 'women/index.html', context=data)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте','menu':menu})

def show_post(request, post_slug):
    """представление показывает пост через слаг, если не нет
     такого совпадения выводится 404 нет такой страницы"""
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        "cat_selected": 1,
    }

    return render(request, 'women/post.html', data)

def addpage(request):
    #  создаем экземпляр класса формы(в зависимости от разновидности запроса POST или GET
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            # пропишем код для добавления данных созданного поста в базу данных
            try:
                Women.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None,"Ошибка добавления поста")
    else:
        form = AddPostForm()

    data = {
        'menu': menu,
        'title': "Добавление статьи",
        'form': form
    }
    """отображает вызов страницы "добавление статьи" """
    return render(request, 'women/addpage.html', data)

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизоваться")

def show_category(request,cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)#переменная с помощью которой будем отбирать катнгорию
    posts = Women.published.filter(cat_id=category.pk).select_related("cat")# добавляем select_related('cat')
    # для использования "жадной" загрузки чтобы не было дублирующих запросов,
    # "cat" это атрибут связывающий ForeignKey в модели Women


    data = {
        'title': f"Рубрика: {category.name}",
        'menu': menu,
        'posts': posts,
        "cat_selected": category.pk,
    }
    return render(request, 'women/index.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def show_tag_postlist(request, tag_slug):
    """функция отображения постов по тэгам"""
    tag = get_object_or_404(TagPost, slug=tag_slug) # читаем запись из таблицы TagPost
    # берём все статьи которые связаны с этим тэгом(через модель Women берём связку related_name='tags'
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')# добавляем select_related('cat')
    # для использования "жадной" загрузки чтобы не было дублирующих запросов,
    # "cat" это атрибут связывающий ForeignKey в модели Women


    data = {
        'title' : f'Тег: { tag.tag }',
        'menu' : menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)
    # после добавим шаблонный тег в women_tags.py