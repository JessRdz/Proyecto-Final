import subprocess
import ipaddress
import platform
import time
import os
from Email import send_notification


def conocer_red():
    dispositivos = []
    f = open("Subnetworks", "r")
    subnets = f.readlines()

    for net_addr in subnets:

        # Subred
        ip_net = ipaddress.ip_network(net_addr.rstrip('\n'))

        # Obtener todos los dispositivos
        all_hosts = list(ip_net.hosts())

        # Hacer ping a cada direccion

        for host in all_hosts:
            # Option for the number of packets as a function of
            param = '-n' if platform.system().lower() == 'windows' else '-c'

            # Building the command. Ex: "ping -c 1 google.com"
            command = ['ping', param, '1', "-w", "100", str(host)]  # ping -n 1 -W 100 10.0.80.1

            if subprocess.call(command, stdout=False) == 0:
                if dispositivos.count(str(host)) == 0:
                    dispositivos.append([str(host), 0])
    return dispositivos


def ping_dispositivos(dispositivos):
    dispositivos_temp = []
    for dispositivo, nivel in dispositivos:
        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', "-w", "100", dispositivo]

        if subprocess.call(command, stdout=False) == 0:
            if nivel > 4:
                mensaje = "Se reanudo la comunicación con el dispositivo " + dispositivo
                send_notification("sonia_gtz05@hotmail.com", "Dispositivo reconectado", mensaje)
                notificar(mensaje)
            nivel = 0
        else:
            nivel = nivel + 1
            if nivel == 3:
                mensaje = "Problemas de comunicacion con " + dispositivo
                send_notification("sonia_gtz05@hotmail.com", "Posible problema de conexion", mensaje)
            if nivel == 5:
                mensaje = "Se interrumpió la comunicación con el dispositivo " + dispositivo
                send_notification("sonia_gtz05@hotmail.com", "Dispositivo desconectado", mensaje)
                notificar(mensaje)

        dispositivos_temp.append([dispositivo, nivel])

    return dispositivos_temp

def notificar(mensaje):
    command = ['notify-send', mensaje]
    subprocess.call(command, stdout=False)

def mostrar(dispositivos):
    print("********************************************\n")
    for dispositivo, nivel in dispositivos:
        if nivel == 0:
            estado = "conectado"
        if nivel >= 3 and nivel < 5:
            estado = "posiblemente desconectado"
        if nivel >= 5:
            estado = "deconectado"
        print(dispositivo + " " + estado)


