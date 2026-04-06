# создаем файл для своего контекстного процессора
# с помощью которого будем передавать menu

from women.views import menu

def get_women_context(request):
    """название произвольное, возвращает словарь,
     который будет доступен во всех шаблонах, обязательно его
     прописываем в settings.py в блоке TEMPLATES"""
    return {'mainmenu': menu}