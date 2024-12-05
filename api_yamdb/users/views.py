from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
# from django.shortcuts import render

from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Новый пользователь."""
    serializer = UserCreationSerializer(data=request.data)    # СМЕНИТЬ СЕРИК
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')

    user, _ = User.objects.get_or_create(username=username, email=email,)
    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        subject="Код подтверждения",
        message=f"Код подтверждения: {confirmation_code}",
        from_email='yamdb@yandex.ru',
        recipient_list=[email],
        fail_silently=False,)

    return Response(serializer.data, status=status.HTTP_200_OK)
