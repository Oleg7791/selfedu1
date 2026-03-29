from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from dns.tsig import get_context
from rest_framework.reverse import reverse_lazy

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles

menu = [
    {'title':'О сайте','url_name':'about'},
    {'title':"Добавить статью",'url_name':'add_page'},
    {'title':"Обратная связь",'url_name':'contact'},
    {'title':"Войти",'url_name':'login'}
]

# заменили на класс WomenHome
# def index(request):  # обязательный параметр request
#
#     posts = Women.published.all().select_related('cat')# добавляем select_related('cat')
#     # для использования "жадной" загрузки чтобы не было дублирующих запросов,
#     # "cat" это атрибут связывающий ForeignKey в модели Women
#
#     data = {
#         'title': "Главная страница",
#         'menu': menu,
#         'posts': posts,
#         "cat_selected": 0,
#     }
#     return render(request, 'women/index.html', context=data)

class WomenHome(ListView):
    """Создаем класс "представления" взамен функции index """
    #model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts' # атрибут присваивает "имя для шаблонов - в index.html"
    # в нашем случае для отображения списка статей
    paginate_by = 2
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        """метод используется для отфильтрованного отображения списка статей"""
        return Women.published.all().select_related('cat')

# заменили в about классом из модели UploadFiles
# def handle_uploaded_file(f):
#     """функция взята из докум-ции django осуществляет загрузку файла, вставляется в about"""
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def about(request):
    """создадим на базе этого метода, метод работы с пагинацией """
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html',
                  {'title':'О сайте', 'page_obj':page_obj})

# пропишем класс представления на замену функции
# def show_post(request, post_slug):
#     """представление показывает пост через слаг, если не нет
#      такого совпадения выводится 404 нет такой страницы"""
#     post = get_object_or_404(Women, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         "cat_selected": 1,
#     }
#
#     return render(request, 'women/post.html', data)

class ShowPost(DetailView):
    """класс представления взамен функции show_post"""
    model = Women
    template_name = 'women/post.html'
    context_object_name = 'post' # сюда нужно записать переменную из post.html
    slug_url_kwarg = 'post_slug' # прописывается переменная из urls.py по которой берется статья

    # def get_queryset(self):
    #     return

    def get_object(self, queryset = None):
        return get_object_or_404(Women.published, slug=self.kwargs['post_slug'])

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

# заменим функцию addpage на класс AddPage
# def addpage(request):
#     #  создаем экземпляр класса формы(в зависимости от разновидности запроса POST или GET
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)# требуется "request.FILES" для передачи файлов
#
#         if form.is_valid():# метод "is_valid" проверяет на валидность(проверка всех параметров в форме)
#             # print(form.cleaned_data)
#
#             # пропишем код для добавления данных созданного поста в базу данных
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None,"Ошибка добавления поста")
#
#             form.save() # сохраняет всё в базу данных
    #         return redirect('home')
    # else:
    #     form = AddPostForm()
    #
    # data = {
    #     'menu': menu,
    #     'title': "Добавление статьи",
    #     'form': form
    # }
    # """отображает вызов страницы "добавление статьи" """
    # return render(request, 'women/addpage.html', data)

# class AddPage(View):
#     """Создаем класс "представления" взамен функции addpage """
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': "Добавление статьи",
#             'form': form
#         }
#         """отображает вызов страницы "добавление статьи" """
#         return render(request, 'women/addpage.html', data)
#
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         data = {
#             'menu': menu,
#             'title': "Добавление статьи",
#             'form': form
#         }
#         """отображает вызов страницы "добавление статьи" """
#         return render(request, 'women/addpage.html', data)

# class AddPage(FormView):
#     """заменим прошлый класс AddPage на новый через класс FormView"""
#     form_class = AddPostForm
#     template_name = 'women/addpage.html'
#     success_url = reverse_lazy('home')
#     extra_context = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#     }
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

class AddPage(CreateView):
    """ещё один вариант класса представления через класс CreateView"""
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }

class UpdatePage(UpdateView):
    """класс представления для обновления поста"""
    model = Women
    fields = ['title','content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Редактирование статьи',
    }

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизоваться")

# # заменим ниже на класс WomenCategory
# def show_category(request,cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)  #переменная с помощью которой будем отбирать катнгорию
#     posts = Women.published.filter(cat_id=category.pk).select_related("cat")  # добавляем
#     # select_related('cat') для использования "жадной" загрузки чтобы не было дублирующих
#     #запросов,"cat" это атрибут связывающий ForeignKey в модели Women
#
#
#     data = {
#         'title': f"Рубрика: {category.name}",
#         'menu': menu,
#         'posts': posts,
#         "cat_selected": category.pk,
#     }
#     return render(request, 'women/index.html', context=data)

class WomenCategory(ListView):
    """класс представления - замена функции show_category"""
    template_name = 'women/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False # атрибут генерирует сообщение 404 при пустом списке('posts')

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# заменяем на класс ShowTagPostList
# def show_tag_postlist(request, tag_slug):
#     """функция отображения постов по тэгам"""
#     tag = get_object_or_404(TagPost, slug=tag_slug) # читаем запись из таблицы TagPost
#     # берём все статьи которые связаны с этим тэгом(через модель Women
#     # берём связку related_name='tags'
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')# добавляем
#     # select_related('cat') для использования "жадной" загрузки чтобы не было дублирующих
#     # запросов,"cat" это атрибут связывающий ForeignKey в модели Women
#
#
#     data = {
#         'title' : f'Тег: { tag.tag }',
#         'menu' : menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'women/index.html', context=data)
#     # после добавим шаблонный тег в women_tags.py

class ShowTagPostList(ListView):
    """создаем класс представления взамен функции 'show_tag_postlist'"""
    template_name = 'women/index.html' # Определяем шаблон.
    context_object_name = 'posts'      # Определяем имя для context_object_name
    allow_empty = False                # Запрещаем пустые списки

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        """ Переопределяем метод get_context_data, сначала вызвав его из родительского класса
         и сохранив в переменную context. Далее добавляем в наш словарь 'context' еще
         несколько ключ-значений."""
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        print(self.kwargs)
        print(tag)
        context['title'] = 'Посты с тегом - ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = 0
        return context
