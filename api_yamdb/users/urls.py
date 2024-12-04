from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, get_jwt_token, signup           # ИСПРАВИТЬ get token

router = DefaultRouter()
router.register("users", UserViewSet)

auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_jwt_token, name='get_jwt_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router.urls)),]  # проверить можно ли оставить '', а в1 перенести в апи_ябд




# urlpatterns = [
#     ...
#     # Djoser создаст набор необходимых эндпоинтов.
#     # базовые, для управления пользователями в Django:
#     path('auth/', include('djoser.urls')),
#     # JWT-эндпоинты, для управления JWT-токенами:
#     path('auth/', include('djoser.urls.jwt')),
# ]