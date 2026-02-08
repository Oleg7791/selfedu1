from django import template
import women.views as views
from women.models import Category

register = template.Library()

@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    """пользовательский тэг для отображения по категориям"""
    cats = Category.objects.all()
    return {'cats':cats,'cat_selected':cat_selected}