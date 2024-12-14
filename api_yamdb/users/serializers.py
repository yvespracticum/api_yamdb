from rest_framework import serializers

from .constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from .models import User


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
    # def validate_username(self, data):
    #     pattern = r"[^a-zA-Z0-9_-]"
    #     match = re.findall(pattern, data)
    #     if match:
    #         raise serializers.ValidationError('Недопустимый символ')
    #     elif data == 'me':
    #         raise serializers.ValidationError('Недопустимое имя')
    #     else:
    #         return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
