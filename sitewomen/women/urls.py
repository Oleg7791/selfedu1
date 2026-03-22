from os import name
from unicodedata import category

from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    #path('', views.index, name='home'),  # http://127/0/0/1/8000/women/ -- ниже пример замены на класс
    path('', views.WomenHome.as_view(), name='home'),
    path('about/',views.about, name='about'),
    #path('addpage/', views.addpage, name='add_page'),-- ниже пример замены на класс
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    #path('post/<slug:post_slug>/', views.show_post, name='post'),-- ниже пример замены на класс
    path('post/<slug:post_slug>/',views.ShowPost.as_view(), name='post'),
    #path('category/<slug:cat_slug>/', views.show_category, name='category')-- ниже замена на класс,
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    # маршрут для отображения тэгов
    #path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag')-- ниже замена на класс,
    path('tag/<slug:tag_slug>/', views.ShowTagPostList.as_view(), name='tag')
]
