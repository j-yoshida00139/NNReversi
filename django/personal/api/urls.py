from .views import BestMoveViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'best_moves', BestMoveViewSet, 'best_move')

urlpatterns = []
urlpatterns += router.urls