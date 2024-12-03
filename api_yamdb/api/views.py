from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)
from reviews.models import Category, Genre, Title


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.prefetch_related('genre').select_related(
        'category'
    )
    serializer_class = TitleSerializer
