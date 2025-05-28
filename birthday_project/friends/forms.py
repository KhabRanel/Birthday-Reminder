from django import forms
from .models import Friend
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Форма регистрации, расширяющая стандартную форму Django.
    Добавляем поле email.
    """

    class Meta:
        model = User
        fields = ('username', 'email')  # Добавляем email к стандартным полям


class FriendForm(forms.ModelForm):
    """
    Форма для добавления/редактирования друга.
    ModelForm автоматически создает поля на основе модели.
    """

    class Meta:
        model = Friend
        fields = ['name', 'birthday']
        widgets = {
            # Используем HTML5 date picker для удобного выбора даты
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }