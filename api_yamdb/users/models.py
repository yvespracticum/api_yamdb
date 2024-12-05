from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from .constants import (USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH,
                        USER, MODERATOR, ADMIN)


class User(AbstractUser):

    ROLE = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    ]

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ')])

    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        blank=False,
        verbose_name='Электронная почта',)

    first_name = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        blank=True,
        verbose_name='Имя')

    last_name = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        blank=True,
        verbose_name='Фамилия')

    bio = models.TextField(
        blank=True,
        verbose_name='О себе')

    role = models.CharField(
        choices=ROLE,
        default=USER,
        verbose_name='Роль пользователя')

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
