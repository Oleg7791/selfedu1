from django import template
import women.views as views
from women.models import Category, TagPost

register = template.Library()

@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats':cats,'cat_selected':cat_selected}

@register.inclusion_tag('women/list_tags.html') #создадим шаблон с названием list_tags.html в women
def show_all_tags(): # воспользуемся им, и перейдем в base.html
    return {'tags': TagPost.objects.all()}