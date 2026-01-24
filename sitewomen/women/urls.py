from os import name

from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    path('', views.index, name='home'),  # http://127/0/0/1/8000/women/
    path('about/',views.about, name='about'),
    path('cats/<int:cat_id>/', views.categories, name='cat_id'),  # http://127/0/0/1/8000/cats/2/
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),  # http://127/0/0/1/8000/cats/ghdf/
    path('archive/<yyyy:year>/', views.archive, name='archive'),
]
