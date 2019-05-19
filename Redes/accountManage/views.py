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
    else:
        flows = Flow.objects.filter(ip_origen=ip_origen)

    # Filtrar flujos por fecha y hora
    bytes = []
    fechas = []
    for flow in flows:
        if flow.fecha >= fecha_ini and flow.fecha <= fecha_fin:
            segundos = flow.duration // 1000 + 1
            band = (float(flow.size)/1000) / segundos
            bytes.append(band)
            fechas.append(flow.fecha.strftime("(%d/%m/%Y) %H:%M"))

    return render(request, 'charts.html', context={'bytes': bytes, 'fechas': fechas, 'ip': ip_origen, 'ip_destino': ip_destino})
