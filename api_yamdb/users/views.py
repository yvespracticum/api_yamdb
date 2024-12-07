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
    UserSerializer,
    SignUpSerializer,
    UserProfileSerializer,
    TokenSerializer
    )


def send_confirmation_code(confirmation_code, email):
    send_mail(
        subject='Код подтверждения',
        message=f'Код подтверждения: {confirmation_code}',
        from_email='yamdb@yandex.ru',
        recipient_list=[email],
        fail_silently=False,)


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
    checkEmail = User.objects.filter(email=email)
    if checkEmail:
        # Если пользователь с таким email уже существует
        checkUsername = User.objects.filter(username=username, email=email)
        if checkUsername:
            # Если существует пользователь с таким email и username
            user = checkUsername.get(email=email)
            confirmation_code = default_token_generator.make_token(user)
            update_user_confirmation_code(user, confirmation_code)
            send_confirmation_code(confirmation_code, email)
            return Response({'message': 'Пользователь с таким email уже есть. '
                            'Код подтверждения отправлен повторно.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Пользователь с таким email и username'
                             'не сущесвует.'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        # Если пользователь с таким username уже существует
        checkUsername = User.objects.filter(username=username)
        if checkUsername:
            return Response({'message': 'Пользователь с таким username '
                             'уже сущесвует.'},
                            status=status.HTTP_400_BAD_REQUEST)
        user, created = User.objects.get_or_create(
            username=username,
            email=email
            )
        confirmation_code = default_token_generator.make_token(user)
        update_user_confirmation_code(user, confirmation_code)
        send_confirmation_code(confirmation_code, email)
        if not created:
            return Response(
                {'message': 'Пользователь с таким email уже есть.'
                 ' Код подтверждения отправлен повторно.'},
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

    return Response(
        {"Неверный код подтверждения."},
        status=status.HTTP_400_BAD_REQUEST,)


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
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
