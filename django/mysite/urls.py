from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^', include('personal.urls')),
	url(r'^api/', include("personal.api.urls", namespace='api')),
]
