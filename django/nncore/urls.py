from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^forward/$', views.forward, name='forward'),
    url(r'^upload_input/$', views.upload_input, name='upload_input'),
]
