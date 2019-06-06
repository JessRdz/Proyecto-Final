from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import View
from .models import Flow



import AnalyzeJson as json
import pytz
from datetime import datetime

# Create your views here.

servicios = ['http']

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
        return render(request, 'charts.html', {})

def cargar_json(request):
    filename = "flows.json"
    flows = json.cargar_json(filename)
    for flow in flows:
        f = Flow(fecha=flow[0], servicio=flow[1], size=flow[2], duration=flow[3], ip_origen=flow[4], ip_destino=flow[5])
        f.save()

    return render(request, 'charts.html', {})

def mostrarFlows(request):

    # Obtener parámetros del POST
    ip_origen = request.POST['ip_source']
    fecha_ini = datetime.strptime(request.POST['fecha_ini'], "%Y-%m-%dT%H:%M")
    fecha_fin = datetime.strptime(request.POST['fecha_fin'], "%Y-%m-%dT%H:%M")
    todo = None
    if request.POST.get('servicios') is not None:
        todo = request.POST['servicios']

    # Configurar zona horaria a las fechas del formulario
    utc = pytz.UTC
    fecha_ini = utc.localize(fecha_ini)
    fecha_fin = utc.localize(fecha_fin)

    # Obtener flujos filtrados por ip
    flows = Flow.objects.all()
    print(todo)
    # Filtrar flujos por fecha y hora
    if ip_origen != '':
        r = routers[ip_origen]
        bytes = []
        fechas = []
        bytes_total = 0
        segundos = 0
        for flow in flows:
            if flow.fecha >= fecha_ini and flow.fecha <= fecha_fin and r.__contains__(flow.ip_origen):
                if todo == '1':
                    print('ha')
                    segundos = segundos + flow.duration // 1000
                    band = float(flow.size) / 1000
                    bytes.append(band)
                    bytes_total = bytes_total + band
                    fechas.append(flow.fecha.strftime("(%d/%m/%Y) %H:%M"))
                else:
                    print('he')
                    if servicios.__contains__(flow.servicio):
                        segundos = segundos + flow.duration // 1000
                        band = float(flow.size) / 1000
                        bytes.append(band)
                        bytes_total = bytes_total + band
                        fechas.append(flow.fecha.strftime("(%d/%m/%Y) %H:%M"))


        return render(request, 'charts.html',
                      context={'bytes': bytes,
                               'bytes_total': bytes_total,
                               'segundos': segundos % 60,
                               'minutos': int(segundos / 60),
                               'fechas': fechas,
                               'ip': ip_origen,
                               'fecha_ini': fecha_ini.strftime("%d/%m/%Y %H:%M"),
                               'fecha_fin': fecha_fin.strftime("%d/%m/%Y %H:%M")})

    else:
        tiempos = {}
        tiempo_total = 0
        bytes = {}
        bytes_total = 0
        for flow in flows:
            if flow.fecha >= fecha_ini and flow.fecha <= fecha_fin:
                if todo == '1':
                    tiempo_total = tiempo_total + float(flow.duration) / 60000
                    if tiempos.get(flow.ip_origen) is None:
                        tiempos[flow.ip_origen] = float(flow.duration) / 60000
                    else:
                        tiempos[flow.ip_origen] = tiempos[flow.ip_origen] + float(flow.duration) / 60000

                    bytes_total = bytes_total + float(flow.size) / 1000
                    if bytes.get(flow.ip_origen) is None:
                        bytes[flow.ip_origen] = float(flow.size) / 1000
                    else:
                        bytes[flow.ip_origen] = bytes[flow.ip_origen] + float(flow.size) / 1000
                else:
                    if servicios.__contains__(flow.servicio):
                        tiempo_total = tiempo_total + float(flow.duration) / 60000
                        if tiempos.get(flow.ip_origen) is None:
                            tiempos[flow.ip_origen] = float(flow.duration) / 60000
                        else:
                            tiempos[flow.ip_origen] = tiempos[flow.ip_origen] + float(flow.duration) / 60000

                        bytes_total = bytes_total + float(flow.size) / 1000
                        if bytes.get(flow.ip_origen) is None:
                            bytes[flow.ip_origen] = float(flow.size) / 1000
                        else:
                            bytes[flow.ip_origen] = bytes[flow.ip_origen] + float(flow.size) / 1000



        return render(request, 'charts.html',
                      context={'bytes': bytes,
                               'total_bytes': bytes_total,
                               'tiempos': tiempos,
                               'total_tiempo': tiempo_total,
                               'fecha_ini': fecha_ini.strftime("%d/%m/%Y %H:%M"),
                               'fecha_fin': fecha_fin.strftime("%d/%m/%Y %H:%M")})