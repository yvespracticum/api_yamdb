from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer, TitleReadSerializer,
)
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)
from users.permissions import IsAdminOrReadOnly, IsOwnerAdminModerator


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'delete')
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'delete')
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer

    def save_and_respond(self, serializer, status_code):
        """
        Общая логика сохранения и возврата данных
        с использованием TitleReadSerializer.
        """
        serializer.is_valid(raise_exception=True)
        self.perform_create(
            serializer
        ) if status_code == status.HTTP_201_CREATED else self.perform_update(
            serializer
        )
        read_serializer = TitleReadSerializer(
            serializer.instance,
            context={'request': self.request}
        )
        return Response(read_serializer.data, status=status_code)

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод create,
        используя общий метод save_and_respond.
        """
        serializer = self.get_serializer(data=request.data)
        return self.save_and_respond(serializer, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Переопределяем метод update,
        используя общий метод save_and_respond.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        return self.save_and_respond(serializer, status.HTTP_200_OK)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerAdminModerator)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer):
        """
        Создает новый отзыв для произведения.
        Проверяет произведение и привязывает к нему отзыв.
        """
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        if Review.objects.filter(title=title,
                                 author=self.request.user).exists():
            raise ValidationError('Вы уже оставляли здесь отзыв.')
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        """
        Возвращает все отзывы для конкретного произведения.
        """
        return Review.objects.filter(title_id=self.kwargs['title_id'])


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerAdminModerator)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        """
        Возвращает все комментарии для конкретного отзыва.
        Проверяет произведение и связанный с ним отзыв.
        """
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id, title=title)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        """
        Создает комментарий для указанного отзыва.
        Проверяет произведение и отзыв, связывает с ним комментарий.
        """
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id, title=title)
        serializer.save(author=self.request.user, review=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
