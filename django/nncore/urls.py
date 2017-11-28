from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^nn_models/$', views.index, name='index'),
]
