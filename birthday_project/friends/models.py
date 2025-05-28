from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    """
    Профиль пользователя - расширение стандартной модели User.
    Связан отношением один-к-одному с User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # ID пользователя в Telegram (может быть пустым)
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)

    # Уникальный код для привязки аккаунта к Telegram
    telegram_code = models.CharField(
        max_length=16,
        unique=True,
        default=uuid.uuid4().hex[:16]  # Генерируем случайный код
    )

    def __str__(self):
        return f'{self.user.username} (Telegram: {self.telegram_id})'


class Friend(models.Model):
    """
    Модель друга с именем и датой рождения.
    Привязан к профилю пользователя.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return f'{self.name} ({self.birthday})'
