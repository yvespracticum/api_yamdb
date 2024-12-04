from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
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


class CommentViewSet(ModelViewSet):   # New
    serializer_class = CommentSerializer

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.comments.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)
