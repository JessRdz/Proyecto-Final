from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
import Puller as pull
from django.views import generic
import requests
import time


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
        context={'dispositivo': pull.mostrarDispositivosWeb()},
    )

