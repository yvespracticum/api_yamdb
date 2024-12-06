from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, get_token, signup

router = DefaultRouter()
router.register('users', UserViewSet)

auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_token, name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
    ]
