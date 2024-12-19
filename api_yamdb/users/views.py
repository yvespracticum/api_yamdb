from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserProfileSerializer,
    UserSerializer,
)


def send_confirmation_code(confirmation_code, email):
    send_mail(
        subject='Код подтверждения',
        message=f'Код подтверждения: {confirmation_code}',
        from_email='yamdb@yandex.ru',
        recipient_list=[email],
    )


def update_user_confirmation_code(user, confirmation_code):
    user.confirmation_code = confirmation_code
    user.save()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Новый пользователь."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    check_email = User.objects.filter(email=email)
    if check_email:
        # Если пользователь с таким email уже существует
        check_username = User.objects.filter(username=username, email=email)
        if check_username:
            # Если существует пользователь с таким email и username
            user = check_username.get(email=email)
            confirmation_code = default_token_generator.make_token(user)
            update_user_confirmation_code(user, confirmation_code)
            send_confirmation_code(confirmation_code, email)
            return Response(
                {
                    'email': email,
                    'username': username
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'email': [email]},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        # Если пользователь с таким username уже существует
        check_username = User.objects.filter(username=username)
        if check_username:
            return Response(
                {
                    'username': [username]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        update_user_confirmation_code(user, confirmation_code)
        send_confirmation_code(confirmation_code, email)
        if not created:
            return Response(
                {
                    'email': [email],
                    'username': [username]
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получения и обновления токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    else:
        return Response(
            {'field_name': ['Неверный код подтверждения.']},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'delete', 'patch']

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH':
            serializer = UserProfileSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
