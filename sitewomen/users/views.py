from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


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

class RegisterUser(CreateView):
    """класс представления формы регистрации"""
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')

# def register(request):
#     """представление для вывода формы регистрации"""
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST) # 'экземпляр формы
#         if form.is_valid():
#             user = form.save(commit=False)# сохраняет в переменную без внесения в БД
#             user.set_password(form.cleaned_data['password'])# метод set_password шифрует
#             # пароль полученный из forms.pt
#             user.save() # сохраняет в БД
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form':form})
#     # связываем с шаблоном URl в urls.py