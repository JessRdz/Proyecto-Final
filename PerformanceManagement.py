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
    host = "50.0.0.2"
    urlRequest = "http://" + host + ":8000/performanceManage/estadisticas/"
    while 1:
        for router, bandera in ips:
                print(str(router) + ":")
                date = time.strftime("%Y-%m-%dT%H:%M")
                for i in range(1, 6):
                    x, status = getSNMP(router, user, password, mibstatus + "." + str(i)).split(" = ")

                    if str(status) == "1":
                        x, interface = getSNMP(router, user, password, mibinterface + "." + str(i)).split(" = ")
                        interface = interface.replace("/", "-")
                        # print(interface)
                        x, value = getSNMP(router, user, password, mibinoctets + "." + str(i)).split(" = ")
                        r = requests.get(urlRequest + date + "/" + router + "/" +
                                         "Interface-in" + "/" + interface + ":" + value)  # value = enp312:100

                        x, value = getSNMP(router, user, password, miboutoctets + "." + str(i)).split(" = ")
                        r = requests.get(urlRequest + date + "/" + router + "/" +
                                         "Interface-out" + "/" + interface + ":" + value)  # value = enp312:100



                # obtener y enviar estadisticas de CPU de cada router
                x, value = getSNMP(router, user, password, mibCPU).split(" = ")
                if value != "No Such Instance currently exists at this OID":
                    r = requests.get(urlRequest + date + "/" + router + "/" +
                                 "CPU" + "/" + value)

                x, value = getSNMP(router, user, password, mibmemory).split(" = ")
                if value != "No Such Object currently exists at this OID":
                    r = requests.get(urlRequest + date + "/" + router + "/" +
                                 "Memory" + "/" + value)

        time.sleep(20)

obtenerEstadisticas()