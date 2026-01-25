from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

menu = [
    {'title':'О сайте','url_name':'about'},
    {'title':"Добавить статью",'url_name':'add_page'},
    {'title':"Обратная связь",'url_name':'contact'},
    {'title':"Войти",'url_name':'login'}
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]


def index(request):  # обязательный параметр request
    # t = render_to_string('women/index.html')
    # return HttpResponse(t)
    data = {
        'title': "главная страница",
        'menu': menu,
        'posts': data_db

    }
    return render(request, 'women/index.html', context=data)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте','menu':menu})

def addpage(request):
    return HttpResponse("Добавление статьи")

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизоваться")

def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id={post_id}")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
