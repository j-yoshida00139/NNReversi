from django.conf.urls import url

from . import ajax
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/nextMove/', ajax.next_move, name='nextMove'),
    url(r'^ajax/storeWinnersData/', ajax.store_winners_data, name='storeWinnersData'),
]
