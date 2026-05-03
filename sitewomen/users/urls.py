from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    #path('login/',views.login_user, name='login') # для функции
    path('login/', views.LoginUser.as_view(), name='login'), # для класса
    #path('logout/', views.logout_user, name='logout'),# для функции
    path('logout/',LogoutView.as_view(), name='logout'),# для класса
    #path('register/', views.register, name='register')
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password-change/',views.UserPasswordChange.as_view(), name="password_change"),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),name="password_change"),
]

