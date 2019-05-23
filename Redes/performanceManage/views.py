from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import View
from django.views import generic
from .models import Estadistica
from datetime import datetime
import pytz
import requests
import time

# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kargs):
        return render(request, 'estadisticas.html', {})


def nueva_estadistica(request, fecha, ip, tipo, valor):
    e = Estadistica(fecha=fecha, ip=ip, tipo=tipo, valor=valor)
    e.save()
    if tipo == 'CPU' and int(valor) >= 80:
        requests.get("http://127.0.0.1:8000/configManage/reportes/" + ip +
                     "/Uso de CPU crítico." + "/" + time.strftime("%c"))
    elif tipo == 'CPU' and 50 <= int(valor) < 80:
        requests.get("http://127.0.0.1:8000/configManage/reportes/" + ip +
                     "/Uso de CPU moderado." + "/" + time.strftime("%c"))

    if tipo == 'Memory' and int(valor) >= 80:
        requests.get("http://127.0.0.1:8000/configManage/reportes/" + ip +
                     "/Uso de memoria crítico." + "/" + time.strftime("%c"))
    elif tipo == 'Memory' and 60 <= int(valor) < 80:
        requests.get("http://127.0.0.1:8000/configManage/reportes/" + ip +
                     "/Uso de memoria moderado." + "/" + time.strftime("%c"))


def mostrarPerformance(request):
    # obtener parametros del POST
    ip = request.POST["ip_source"]
    fechaini = datetime.strptime(request.POST["fecha_ini"], "%Y-%m-%dT%H:%M")
    fechafin = datetime.strptime(request.POST["fecha_fin"], "%Y-%m-%dT%H:%M")
    fechaini = pytz.UTC.localize(fechaini)
    fechafin = pytz.UTC.localize(fechafin)

    # obtener datos filtrados
    fechascpu = []
    cpu = []
    fechasmemory = []
    memoria = []
    fechasinterin = []
    """
    interfazin =
        {
            "fa0/0":[0,4,5,6],
            "fa0/1":[2,3,5,1]
        }
    """
    fechasinterout = []
    interfazin = {}
    interfazout = {}
    estadisticas = Estadistica.objects.filter(ip=ip)

    for estadistica in estadisticas:
        if fechaini <= estadistica.fecha <= fechafin:
            f = estadistica.fecha.strftime("(%d/%m/%Y) %H:%M")

            if estadistica.tipo == "CPU":
                cpu.append(int(estadistica.valor))
                fechascpu.append(f)

            elif estadistica.tipo == "Interface-in":
                interface, valor = estadistica.valor.split(":")

                if interfazin.get(interface) is None:
                    interfazin[interface] = []

                interfazin[interface].append(int(valor))
                fechasinterin.append(f)

            elif estadistica.tipo == "Interface-out":
                interface, valor = estadistica.valor.split(":")

                if interfazout.get(interface) is None:
                    interfazout[interface] = []

                interfazout[interface].append(int(valor))
                fechasinterout.append(f)

            elif estadistica.tipo == "Memory":
                memoria.append(int(estadistica.valor))
                fechasmemory.append(f)

    fechasinterout = list(set(fechasinterout))
    fechasinterin = list(set(fechasinterin))
    return render(request, 'estadisticas.html', {'fechasCPU': fechascpu,
                                                 'fechasMemoria': fechasmemory,
                                                 'fechasInterfazIn': fechasinterin,
                                                 'fechasInterfazOut': fechasinterout,
                                                 'valoresCPU': cpu,
                                                 'valoresMemoria': memoria,
                                                 'valoresInterfazIn': interfazin,
                                                 'valoresInterfazOut': interfazout,
                                                 'ip': ip,
                                                 'fecha_ini': fechaini.strftime("%d/%m/%Y %H:%M"),
                                                 'fecha_fin': fechafin.strftime("%d/%m/%Y %H:%M")
                                                 })

