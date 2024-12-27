from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (
    CATEGORY_NAME_MAX_LENGHT,
    GENRE_NAME_MAX_LENGHT,
    TITLE_NAME_MAX_LENGHT,
)

User = get_user_model()


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(max_length=TITLE_NAME_MAX_LENGHT)
    year = models.PositiveSmallIntegerField()
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField('Genre', related_name='titles')
    category = models.ForeignKey(
        'Category',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории произведения."""
    name = models.CharField(max_length=CATEGORY_NAME_MAX_LENGHT)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""
    name = models.CharField(max_length=GENRE_NAME_MAX_LENGHT)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Модель отзыва на произведение.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ('author', 'title')

    def save(self, *args, **kwargs):
        """Переопределяем save для пересчета рейтинга при добавлении отзыва."""
        super().save(*args, **kwargs)
        self.update_title_rating()

    def delete(self, *args, **kwargs):
        """Переопределяем delete для пересчета рейтинга при удалении отзыва."""
        title = self.title
        super().delete(*args, **kwargs)
        title.save()

    def update_title_rating(self):
        """Пересчитывает рейтинг для связанного произведения."""
        title = self.title
        reviews = title.reviews.all()
        scores = [review.score for review in reviews]
        if scores:
            title.rating = sum(scores) // len(scores)
        else:
            title.rating = None
        title.save()


class Comment(models.Model):
    """
    Модель комментария к отзыву на произведение.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
