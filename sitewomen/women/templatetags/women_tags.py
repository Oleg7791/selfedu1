from django import template
from django.db.models import Count

import women.views as views
from women.models import Category, TagPost

register = template.Library()

@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(x=Count('posts')).filter(x__gt=0)
    return {'cats':cats,'cat_selected':cat_selected}

@register.inclusion_tag('women/list_tags.html') #создадим шаблон с названием list_tags.html в women
def show_all_tags(): # воспользуемся им, и перейдем в base.html
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}