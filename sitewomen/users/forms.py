from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    """класс создающий форму для авторизации"""

    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username','password']

class RegisterUserForm(forms.ModelForm):
    """класс создающий форму для регистрации пользователя"""
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password','password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': "Фамилия "
        }

    def clean_password2(self):
        """метод-валидатор проверяет соответствие пароля"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password']

    def clean_email(self):
        """метод-валидатор проверяет уникальность email"""
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():# проверяет есть ли
            # в модели пользователь с таким email
            raise forms.ValidationError("Такой E-mail уже существует")
        return email
