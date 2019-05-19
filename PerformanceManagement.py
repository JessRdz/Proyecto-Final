import threading
import Puller
import time
from SNMPget import getSNMP
import requests

# SNMP v3 auth
user = "demo"
password = "password"

# mibs
mibSysdesc = "1.3.6.1.2.1.1.1.0"
chasisId = "1.3.6.1.4.1.9.3.6.3.0"
mibinterface = "1.3.6.1.2.1.2.2.1.2"
mibstatus = "1.3.6.1.2.1.2.2.1.7"
mibinoctets = "1.3.6.1.2.1.2.2.1.10"
miboutoctets = "1.3.6.1.2.1.2.2.1.16"
mibCPU = "1.3.6.1.4.1.9.9.109.1.1.1.1.5"
mibmemory = "1.3.6.1.4.1.9.9.109.1.1.1.1.12"

#1.3.6.1.4.1.9.3.6.11 card table
#1.3.6.1.4.1.9.3.6.11.1 card table entry
#1.3.6.1.4.1.9.3.6.11.1.3 card des
#1.3.6.1.4.1.9.3.6.11.1.4 card serial
#1.3.6.1.4.1.9.3.6.3 chassis id

def obtenerEstadisticas():
    ips = Puller.conocer_red()
    ips.remove(["50.0.0.2", 0])
    urlRequest = "http://127.0.0.1:8000/performanceManage/estadisticas/"
    while 1:
        for router, bandera in ips:
            try:
                for i in range(1, 6):
                    x, status = getSNMP(router, user, password, mibstatus + "." + str(i)).split("=")
                    if status == 1:
                        x, interface = getSNMP(router, user, password, mibinterface + "." + str(i)).split("=")

                        x, value = getSNMP(router, user, password, mibinoctets + "." + str(i)).split("=")
                        r = requests.get(urlRequest + time.strftime("%c") + "/" + router +
                                         "Interface-in" + "/" + interface + ":" + value)  # value = enp312:100

                        x, value = getSNMP(router, user, password, miboutoctets + "." + str(i)).split("=")
                        r = requests.get(urlRequest + time.strftime("%c") + "/" + router +
                                         "Interface-out" + "/" + interface + ":" + value)  # value = enp312:100

                # obtener y enviar estadisticas de CPU de cada router
                x, value = getSNMP(router, user, password, mibCPU).split("=")
                r = requests.get(urlRequest + time.strftime("%c") + "/" + router +
                                 "CPU" + "/" + value)

                x, value = getSNMP(router, user, password, mibmemory).split("=")
                r = requests.get(urlRequest + time.strftime("%c") + "/" + router +
                                 "Memory" + "/" + value)

            except:
                print("Falló la comunicación con " + router + "...")

        time.sleep(20)

obtenerEstadisticas()