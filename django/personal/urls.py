from django.conf.urls import url
from . import views
from . import ajax
from .views import BestMoveViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'best_moves', BestMoveViewSet, 'best_move')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/nextMove/', ajax.next_move, name='nextMove'),
    url(r'^ajax/storeWinnersData/', ajax.store_winners_data, name='storeWinnersData'),
]
urlpattern = []
urlpattern += router.urls
