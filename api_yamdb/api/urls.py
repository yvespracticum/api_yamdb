from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet,
                       GenreViewSet, TitleViewSet)

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(r'titles/(?P<title_id>\d+)/comments',
                CommentViewSet, basename='comments')  # New

urlpatterns = router.urls
