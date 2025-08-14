from rest_framework.routers import DefaultRouter
from .views import LieuViewSet

router = DefaultRouter()
router.register('', LieuViewSet, basename='lieu')

urlpatterns = router.urls
