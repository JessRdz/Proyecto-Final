from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
import ConfigurationManagement as config
from django.views import generic
from .models import Reporte

# Create your views here.
def index(request):
	# Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        # context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )

def ver_dispositivos(request):
    return render(
        request,
        'index.html',
        context={'dispositivos': config.mostrarInventarioWeb(config.obtenerInventarioWeb())},
    )

def nuevo_reporte(request, ip, descripcion, fecha):
    r = Reporte(ip=ip, descripcion=descripcion, fecha=fecha)
    r.save()
    success_url = reverse_lazy('reportes')

class ReporteListView(generic.ListView):
    model = Reporte

class ReporteDelete(DeleteView):
    model = Reporte
    success_url = reverse_lazy('reportes')