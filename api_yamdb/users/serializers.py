from rest_framework import serializers

from .models import User
from .constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH


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
        regex=r'^[\w.@+-]'
        )
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        required=True,
        )

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError('Недопустимое имя')
        return data

    def validate(self, data):
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
                )

        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
                )

        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')