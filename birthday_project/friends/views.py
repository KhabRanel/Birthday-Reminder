from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegisterForm, FriendForm
from .models import Friend, Profile
import uuid
from datetime import date, timedelta


def index_view(request):
    """
    Главная страница с описанием проекта.
    Доступна всем пользователям.
    """
    return render(request, 'friends/index.html')


def about_view(request):
    """
    Страница "О проекте".
    Статичная страница с информацией.
    """
    return render(request, 'friends/about.html')


def register_view(request):
    """
    Регистрация нового пользователя.
    После успешной регистрации создаем профиль и логиним пользователя.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save()

            # Создаем профиль для пользователя
            # Это важно! Без профиля пользователь не сможет добавлять друзей
            Profile.objects.create(user=user)

            # Автоматически логиним пользователя после регистрации
            login(request, user)

            # Перенаправляем на список друзей
            return redirect('friend_list')
    else:
        # GET запрос - показываем пустую форму
        form = RegisterForm()

    return render(request, 'friends/register.html', {'form': form})


@login_required  # Декоратор - только для авторизованных пользователей
def friend_list_view(request):
    """
    Список друзей пользователя с группировкой по датам.
    Это самое важное представление - показывает друзей по категориям.
    """
    # Получаем всех друзей текущего пользователя
    friends = Friend.objects.filter(profile=request.user.profile)
    # Получаем сегодняшнюю дату и завтрашнюю
    today = date.today()
    tomorrow = today + timedelta(days=1)
    # Создаем списки для группировки
    friends_today = []
    friends_tomorrow = []
    other_friends = []
    # Группируем друзей по датам
    for friend in friends:
        # Проверяем, совпадает ли день и месяц рождения с сегодняшней датой
        if friend.birthday.month == today.month and friend.birthday.day == today.day:
            friends_today.append(friend)
        # Проверяем завтрашнюю дату
        elif friend.birthday.month == tomorrow.month and friend.birthday.day == tomorrow:
            friends_tomorrow.append(friend)
        else:
            # Все остальные друзья
            other_friends.append(friend)
    # Передаем все группы в шаблон
    context = {
        'friends_today': friends_today,
        'friends_tomorrow': friends_tomorrow,
        'other_friends': other_friends,
    }
    return render(request, 'friends/friend_list.html', context)


@login_required
def add_friend_view(request):
    """
    Добавление нового друга.
    """
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            # Сохраняем форму, но не записываем в БД (commit=False)
            friend = form.save(commit=False)

            # Привязываем друга к профилю текущего пользователя
            friend.profile = request.user.profile

            # Теперь сохраняем в БД
            friend.save()

            # Перенаправляем на список друзей
            return redirect('friend_list')
    else:
        # GET запрос - показываем пустую форму
        form = FriendForm()

    return render(request, 'friends/add_friend.html', {'form': form})


@login_required
def edit_friend_view(request, friend_id):
    """
    Редактирование существующего друга.
    """
    # Получаем друга или возвращаем 404, если не найден
    # Важно: проверяем, что друг принадлежит текущему пользователю!
    friend = get_object_or_404(Friend, id=friend_id, profile=request.user.profile)

    if request.method == 'POST':
        # Передаем instance - это говорит форме, что мы редактируем существующий объек
        form = FriendForm(request.POST, instance=friend)
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('friend_list')
    else:
        # GET запрос - показываем форму с текущими данными
        form = FriendForm(instance=friend)

    return render(request, 'friends/edit_friend.html', {'form': form})


@login_required
def delete_friend_view(request, friend_id):
    """
    Удаление друга с подтверждением.
    """
    friend = get_object_or_404(Friend, id=friend_id, profile=request.user.profile)

    if request.method == 'POST':
        # Пользователь подтвердил удаление
        friend.delete()
        return redirect('friend_list')

    # GET запрос - показываем страницу подтверждения
    return render(request, 'friends/delete_friend.html', {'friend': friend})


@login_required
def telegram_link_view(request):
    """
    Страница для привязки аккаунта к Telegram.
    Показывает код для связывания или информацию о уже привязанном аккаунте.
    """
    profile = request.user.profile
    return render(request, 'friends/telegram_link.html', {'profile': profile})


@login_required
def generate_new_code_view(request):
    """
    Генерация нового кода для привязки к Telegram.
    """
    profile = request.user.profile

    # Генерируем новый уникальный код
    profile.telegram_code = uuid.uuid4().hex[:16]
    profile.save()

    return redirect('telegram_link')


@login_required
def unlink_telegram_view(request):
    """
    Отвязка аккаунта от Telegram.
    """
    profile = request.user.profile

    # Удаляем telegram_id (устанавливаем в None)
    profile.telegram_id = None
    profile.save()

    return redirect('telegram_link')
