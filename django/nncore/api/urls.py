from .views import NNMoveViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'nn_move', NNMoveViewSet, 'nn_move')

urlpatterns = []
urlpatterns += router.urls
