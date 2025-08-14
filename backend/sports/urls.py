from rest_framework.routers import DefaultRouter
from .views import SportViewSet

router = DefaultRouter()
router.register('', SportViewSet, basename='sport')

urlpatterns = router.urls
