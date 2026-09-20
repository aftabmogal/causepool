from rest_framework.routers import DefaultRouter
from .views import DrawResultViewSet, MyWinsViewSet

router = DefaultRouter()
router.register("results", DrawResultViewSet, basename="draw-result")
router.register("my-wins", MyWinsViewSet, basename="my-wins")
urlpatterns = router.urls
