from django.conf.urls import url, include
from . import views
from . import ajax

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^ajax/test/', ajax.test, name='ajax'),
]
