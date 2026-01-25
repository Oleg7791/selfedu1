from os import name

from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    path('', views.index, name='home'),  # http://127/0/0/1/8000/women/
    path('about/',views.about, name='about'),
    path('post/<int:post_id>/', views.show_post, name='post'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
]
