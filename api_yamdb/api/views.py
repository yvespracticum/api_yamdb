from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)
from reviews.models import Category, Genre, Title
from users.permissions import IsAdminOrReadOnly


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'delete')

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'delete')

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.prefetch_related('genre').select_related(
        'category'
    )
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'delete')

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
