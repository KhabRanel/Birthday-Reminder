from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),

    # Аутентификация
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='friends/login.html',  # Указываем свой шаблон
        redirect_authenticated_user=True  # Перенаправляем уже авторизованных
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # Управление друзьями
    path('friend-list/', views.friend_list_view, name='friend_list'),
    path('add/', views.add_friend_view, name='add_friend'),
    path('edit/<int:friend_id>/', views.edit_friend_view, name='edit_friend'),
    path('delete/<int:friend_id>/', views.delete_friend_view, name='delete_friend'),
    # Telegram интеграция
    path('telegram/', views.telegram_link_view, name='telegram_link'),
    path('telegram/new-code/', views.generate_new_code_view, name='generate_new_code'),
    path('telegram/unlink/', views.unlink_telegram_view, name='unlink_telegram'),
]
