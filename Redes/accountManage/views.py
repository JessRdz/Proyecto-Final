from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import View
from .models import Flow

from rest_framework.views import APIView
from rest_framework.response import Response

import AnalyzeJson as json
import pytz
from datetime import datetime

# Create your views here.

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
    ip_destino = request.POST['ip_destino']
    fecha_ini = datetime.strptime(request.POST['fecha_ini'], "%Y-%m-%dT%H:%M")
    fecha_fin = datetime.strptime(request.POST['fecha_fin'], "%Y-%m-%dT%H:%M")

    # Configurar zona horaria a las fechas del formulario
    utc = pytz.UTC
    fecha_ini = utc.localize(fecha_ini)
    fecha_fin = utc.localize(fecha_fin)

    # Obtener flujos filtrados por ip
    if ip_origen != '' and ip_destino != '':
        flows = Flow.objects.filter(ip_origen=ip_origen, ip_destino=ip_destino)
    elif ip_destino != '':
        flows = Flow.objects.filter(ip_destino=ip_destino)
    elif ip_origen != '':
        flows = Flow.objects.filter(ip_origen=ip_origen)
    else:
        flows = Flow.objects.all()

    # Filtrar flujos por fecha y hora
    if ip_origen != '' or ip_destino != '':
        bytes = []
        fechas = []
        for flow in flows:
            if flow.fecha >= fecha_ini and flow.fecha <= fecha_fin:
                segundos = flow.duration // 1000 + 1
                band = float(flow.size) / 1000
                bytes.append(band)
                fechas.append(flow.fecha.strftime("(%d/%m/%Y) %H:%M"))
        return render(request, 'charts.html',
                      context={'bytes': bytes,
                               'fechas': fechas,
                               'ip': ip_origen,
                               'ip_destino': ip_destino})

    else:
        tiempos = {}
        tiempo_total = 0
        bytes = {}
        bytes_total = 0
        for flow in flows:
            if flow.fecha >= fecha_ini and flow.fecha <= fecha_fin:

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