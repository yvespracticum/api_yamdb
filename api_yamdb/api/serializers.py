from datetime import datetime

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category'
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category'
        )

    def create(self, validated_data):
        """
        Получаем или создаем категорию «Без категории»,
        если она не передана.
        """
        if 'category' not in validated_data:
            default_category, _ = Category.objects.get_or_create(
                name='Без категории', slug='no-category'
            )
            validated_data['category'] = default_category

        return super().create(validated_data)

    def validate_category(self, value):
        """Проверяем, что поле category не пустое."""
        if not value:
            raise serializers.ValidationError(
                'Поле category не может быть пустым.'
            )
        return value

    def validate_year(self, value):
        """
        Проверяем, что год не превышает текущий.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего года.'
            )
        return value

    def validate_genre(self, value):
        """Проверяем, что поле genre не пустое."""
        if not value:
            raise serializers.ValidationError(
                'Поле genre не может быть пустым.'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title', 'author', 'pub_date')

    def validate(self, data):
        """Проверяет, что пользователь не оставил
        более одного отзыва к одному произведению."""
        request = self.context.get('request')
        title_id = self.context['view'].kwargs.get('title_id')
        if request.method == 'POST' and Review.objects.filter(
            title_id=title_id,
            author=request.user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review', 'author', 'pub_date')
