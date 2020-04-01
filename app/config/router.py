from rest_framework import routers

from api.viewsets import BlueprintTestViewSet, BlueprintViewSet

router = routers.DefaultRouter()
router.register('test', BlueprintTestViewSet, basename='api_test')
router.register('', BlueprintViewSet, basename='api_blueprint')
