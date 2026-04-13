from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from users.forms import LoginUserForm

# ниже напишем стандартный класс Авторизации взамен функции
# def login_user(request):
#     """функция аутентификации пользователя"""
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,username=cd['username'],
#                                  password=cd['password']) # username берется из forms.py
#             if user and user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

class LoginUser(LoginView):
    """класс авторизации"""
    form_class = LoginUserForm # наследуется от (AuthenticationForm в forms.py-класс загружающий форму)
    template_name = 'users/login.html' # имя шаблона
    extra_context = {'title': "Авторизация"} # имя переменной передаваемой в шаблон

    def get_success_url(self):
        """метод возвращает нас на указанную нами страницу
         в случае успешной авторизации, можно заменить на константу
         в settings.py "LOGIN_REDIRECT_URL = 'home'" """
        return reverse_lazy('home')

# заменили классом в urls.py
# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))