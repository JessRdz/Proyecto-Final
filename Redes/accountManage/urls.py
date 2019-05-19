from django.urls import path
from django.conf.urls import url
from django.contrib import admin

from . import views


urlpatterns = [
	url(r'^$', views.HomeView.as_view(), name='home'),
	path("actualizarFlows", views.cargar_json),
	path("mostrarFlows", views.mostrarFlows),
	# url(r'^reportes/$', views.ReporteListView.as_view(), name='reportes'),
	# url(r"^reportes/(?P<ip>[^/]+)/(?P<descripcion>[^/]+)/(?P<fecha>[^/]+)/$", views.nuevo_reporte)
]