from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^forward/$', views.forward, name='forward'),
	url(r'^train/$', views.train, name='train'),
]
