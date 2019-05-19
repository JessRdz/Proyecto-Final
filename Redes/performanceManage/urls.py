from django.urls import path
from django.conf.urls import url
from django.contrib import admin

from . import views


urlpatterns = [
	url(r'^estadisticas/$', views.HomeView.as_view(), name='estadistica'),
    url(r"^estadisticas/(?P<fecha>[^/]+)/(?P<ip>[^/]+)/(?P<tipo>[^/]+)/(?P<valor>[^/]+)/$", views.nueva_estadistica),
    path("estadisticas/mostrarPerformance", views.mostrarPerformance),
]