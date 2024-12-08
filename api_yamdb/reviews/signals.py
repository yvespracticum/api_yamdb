from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from reviews.models import Review


@receiver((post_save, post_delete), sender=Review)
def update_rating(sender, instance, **kwargs):
    """
    Пересчитывает рейтинг произведения
    при добавлении, изменении или удалении отзыва.
    """
    title = instance.title
    reviews = title.reviews.all()
    scores = [review.score for review in reviews]

    if scores:
        rating = sum(scores) / len(scores)
        title.rating = round(rating, 1)
    else:
        title.rating = None
    title.save()
