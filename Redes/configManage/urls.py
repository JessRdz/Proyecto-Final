from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	path("obtenerInventario", views.ver_dispositivos),
	path("verificarConfiguracion", views.verificar_configuracion),
	url(r'^reportes/$', views.ReporteListView.as_view(), name='reportes'),
	url(r"^reportes/(?P<ip>[^/]+)/(?P<descripcion>[^/]+)/(?P<fecha>[^/]+)/$", views.nuevo_reporte)
]