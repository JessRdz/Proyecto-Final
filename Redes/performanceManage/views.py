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
import operator
from datetime import datetime
import pytz

# Create your views here.

host = "10.10.10.83"
routers = {'R2': ['50.0.0.1', '10.0.80.2', '10.0.80.5'],
           'R1': ['10.0.80.1', '10.0.80.13'],
           'R3': ['10.0.80.6', '10.0.80.14', '10.0.80.9'],
           'R4': ['10.0.80.10', '172.16.200.1'],
           'R5': ['172.16.200.2', '172.16.200.5', '172.16.200.10'],
           'R6': ['172.16.200.9', '172.16.200.14'],
           'R7': ['172.16.200.13'],
           'R8': ['172.16.200.6']}

class HomeView(View):
    def get(self, request, *args, **kargs):
        return render(request, 'estadisticas.html', {})


def nueva_estadistica(request, fecha, ip, tipo, valor):
    fe = datetime.strptime(fecha, "%Y-%m-%dT%H:%M")
    utc = pytz.UTC
    fe = utc.localize(fe)
    e = Estadistica(fecha=fe, ip=ip, tipo=tipo, valor=valor)
    e.save()
    if tipo == 'CPU' and int(valor) >= 80:
        requests.get("http://" + host + ":8000/configManage/reportes/" + ip +
                     "/Uso de CPU crítico." + "/" + time.strftime("%c"))
    elif tipo == 'CPU' and 50 <= int(valor) < 80:
        requests.get("http://" + host + ":8000/configManage/reportes/" + ip +
                     "/Uso de CPU moderado." + "/" + time.strftime("%c"))

    if tipo == 'Memory' and int(valor) >= 80:
        requests.get("http://" + host + ":8000/configManage/reportes/" + ip +
                     "/Uso de memoria crítico." + "/" + time.strftime("%c"))
    elif tipo == 'Memory' and 60 <= int(valor) < 80:
        requests.get("http://" + host + "/configManage/reportes/" + ip +
                     "/Uso de memoria moderado." + "/" + time.strftime("%c"))


def mostrarPerformance(request):
    # obtener parametros del POST
    router = request.POST["ip_source"]
    ip = ""
    print(router)
    try:
        ip = routers[router][0]
    except:
        return render(request, 'estadisticas.html')

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

def mostrar10Links(request):
    estadisticas = Estadistica.objects.filter(tipo='Interface-in')
    interfaces = {}
    dispositivo = ""
    for estadistica in estadisticas:
        interfaz, x = str(estadistica.valor).split(':')
        for r in routers.items():
            print(r[1])
            if r[1].__contains__(estadistica.ip):
                dispositivo = r[0]
                print(dispositivo)
                break
        interfaz = dispositivo + ': ' + interfaz
        if interfaces.get(interfaz) is None:
            interfaces[interfaz] = 0
        interfaces[interfaz] = interfaces[interfaz] + int(x)

    inter = []
    for i in interfaces.items():
        inter.append(i)
    inter.sort(key=lambda x: x[1])
    inter.reverse()

    return render(request, 'estadisticas.html', {'interfaces': inter[0:10]})
