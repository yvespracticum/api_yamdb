import re

from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

from .constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from .models import User
from .send_code import send_confirmation_code


def update_user_confirmation_code(user, confirmation_code):
    user.confirmation_code = confirmation_code
    user.save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        regex=r'^[\w.@+-]',
    )

    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        required=True,
    )

    def validate_username(self, data):
        pattern = re.compile(r'^[\w.@+-]+\Z')
        if not pattern.match(data):
            raise serializers.ValidationError('Недопустимый символ')
        elif data == 'me':
            raise serializers.ValidationError('Недопустимое имя')
        return data

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email."""
        username = data.get('username')
        email = data.get('email')
        if not User.objects.filter(
            username=username, email=email
        ).exists():
            if User.objects.filter(username=username):
                raise serializers.ValidationError(
                    {'username': [username]}
                )

            if User.objects.filter(email=email):
                raise serializers.ValidationError(
                    {'email': [email]}
                )

        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        update_user_confirmation_code(user, confirmation_code)
        send_confirmation_code(confirmation_code, user.email)
        return user


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
