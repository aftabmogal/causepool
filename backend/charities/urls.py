from rest_framework.routers import DefaultRouter
from .views import CharityViewSet

router = DefaultRouter()
router.register("", CharityViewSet, basename="charity")
urlpatterns = router.urls
