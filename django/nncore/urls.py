from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^forward/$', views.forward, name='forward'),
	# url(r'^api/', include("api.urls", namespace='api')),
]
