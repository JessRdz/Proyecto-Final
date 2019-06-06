import os
import re

routers = {'R2': ['50.0.0.1', '10.0.80.2', '10.0.80.5'],
           'R1': ['10.0.80.1', '10.0.80.13'],
           'R3': ['10.0.80.6', '10.0.80.14', '10.0.80.9'],
           'R4': ['10.0.80.10', '172.16.200.1'],
           'R5': ['172.16.200.2', '172.16.200.5', '172.16.200.10'],
           'R6': ['172.16.200.9', '172.16.200.14'],
           'R7': ['172.16.200.13'],
           'R8': ['172.16.200.6']}

class Router:
    def __init__(self):
        self.hostname = ""
        self.interfaces = []
        self.eigrp = {'networks': [],
                      'redistribute': []}
        self.ospf = {'networks': [],
                     'redistribute': []}
        self.snmp = {'user': '',
                     'version': 3,
                     'host': ''}
        self.tftp = {'nvram': 'startup-config'}

    def __repr__(self):
        return self.hostname + "\n" \
                               "Interfaces: " + str(self.interfaces) + "\n" \
                               "EIGRP: " + str(self.eigrp) + "\n" \
                               "OSPF: " + str(self.ospf) + "\n" \
                               "SNMP: " + str(self.snmp) + "\n" \
                               "TFTP: " + str(self.tftp)

    def from_string(self, cadena):
        # Obtener hostname
        hostpat = re.compile('hostname:(\w+)')
        match = hostpat.search(cadena)
        x, self.hostname = match.group().split(":")

        # Obtener interfaces
        interpat = re.compile('interfaces{([\w\s":,./]+)}')
        match = interpat.search(cadena)
        lines = match.group().split("\n")
        for line in lines:
            if not (line.__contains__("{") or line.__contains__("}")):
                inter, desc = line.split(",")
                nombre, ip, mask = inter.split(":")
                self.interfaces.append((nombre, ip, mask))

        # Obtener eigrp
        eigrpat = re.compile('eigrp{([\w\s":,./|]+)}')
        match = eigrpat.search(cadena)
        if match is not None:
            lines = match.group().split("\n")
            for line in lines:
                if not (line.__contains__("{") or line.__contains__("}")):
                    key, valor, desc = line.split(":")
                    if key == 'networks':
                        for v in valor.split(","):
                            ip, wild = v.split("|")
                            self.eigrp[key].append((ip,wild))
                    else:
                        self.eigrp[key] = valor.split(",")

        # Obtener ospf
        ospfpat = re.compile('ospf{([\w\s":,./|]+)}')
        match = ospfpat.search(cadena)
        if match is not None:
            lines = match.group().split("\n")
            for line in lines:
                if not (line.__contains__("{") or line.__contains__("}")):
                    key, valor, desc = line.split(":")
                    if key == 'networks':
                        for v in valor.split(","):
                            ip, mask, area = v.split("|")
                            self.ospf[key].append((ip, mask, area))
                    else:
                        self.ospf[key] = valor.split(",")

        # Obtener snmp
        ospfpat = re.compile('snmp{([\w\s":,./|]+)}')
        match = ospfpat.search(cadena)
        if match is not None:
            lines = match.group().split("\n")
            for line in lines:
                if not (line.__contains__("{") or line.__contains__("}")):
                    valor, desc = line.split(",")
                    key, valor = valor.split(":")
                    self.snmp[key] = valor

        # Obtener tftp
        ospfpat = re.compile('tftp{([\w\s":,./|]+)}')
        match = ospfpat.search(cadena)
        if match is not None:
            lines = match.group().split("\n")
            for line in lines:
                if not (line.__contains__("{") or line.__contains__("}")):
                    valor, desc = line.split(",")
                    key, valor = valor.split(":")
                    self.snmp[key] = valor

    def from_conf_file(self, cadena):
        # Obtener hostname
        hostpat = re.compile('hostname (\w+)')
        match = hostpat.search(cadena)
        x, self.hostname = match.group().split(" ")

        # Obtener interfaces
        interpat = re.compile('interface ([\w/]+)\n ip address ([\d.]+) ([\d.]+)')
        match = interpat.findall(cadena)
        for nombre, ip, mask in match:
            self.interfaces.append((nombre, ip, mask))

        #Obtener eigrp
        eigrpat = re.compile('router eigrp 100\n( redistribute [\w ]+\n)*( network [\d.]+ [\d.]+\n)* ')
        match = eigrpat.search(cadena)
        for l in match.group().split('\n')[1:-1]:
            v = l.split(' ')
            if v[1] == 'redistribute':
                self.eigrp[v[1]].append(str(v[2]) + str(v[3]))
            else:
                self.eigrp[str(v[1]) + 's'].append((v[2], v[3]))

        # Obtener ospf
        ospfpat = re.compile('router ospf 1\n[ log\-adjacency\-changes\n]*'
                             '( redistribute [\w ]+\n)*( network [\d.]+ [\d.]+ area \d\n)*!')
        match = ospfpat.search(cadena)
        for l in match.group().split('\n')[2:-1]:
            v = l.split(' ')
            if v[1] == 'redistribute':
                self.ospf[v[1]].append(str(v[2]) + " " + str(v[3]))
            else:
                self.ospf[str(v[1]) + 's'].append((v[2], v[3], v[5]))

        # Obtener snmp
        ospfpat = re.compile('snmp-server host ([\d.]+) version (\d) auth ([\w ]+)')
        host, version, ip = ospfpat.findall(cadena)[0]
        self.snmp['host'] = host
        self.snmp['version'] = version
        self.snmp['user'] = ip

        # Obtener tftp
        ospfpat = re.compile('tftp-server nvram:([\w ]+)')
        match = ospfpat.search(cadena)[0]


def obtener_routers_template():
    templates = open("template")
    contenido = templates.read()
    routers = contenido.split("***************************************************")
    resultado = []
    for router in routers:
        r = Router()
        r.from_string(router)
        resultado.append(r)
    return resultado

def obtener_router_archivo(archivo):
    conf = open('archivos/' + archivo)
    contenido = conf.read()
    r = Router()
    r.from_conf_file(contenido)
    return r

def obtener_diferencias(rconf, rtemp):
    resultado = ""
    if rconf.hostname != rtemp.hostname:
        resultado = resultado + "<tr><td>Hostname</td><td>" + rtemp.hostname + "</td><td>" + rconf.hostname + "</td></tr>"
    for interface in rconf.interfaces:
        for interfacetemp in rtemp.interfaces:
            if interface[0] == interfacetemp[0] and (interface[1] != interfacetemp[1] or interface[2] != interfacetemp[2]):
                resultado = resultado + "" \
                            "<tr><td>" + interface[0] + "</td><td>" + interfacetemp[1] + ":" + interfacetemp[2] + "" \
                            "</td><td>" + interface[1] + ":" + interface[2] + "</td></tr>"

   #Comparacion EIGRP
    tempnet = ""
    for net in rtemp.eigrp["networks"]:
        if not rconf.eigrp["networks"].__contains__(net):
            tempnet = tempnet + net + ", "
    if tempnet != "":
        resultado = resultado + "<tr><td> EIGRP networks </td><td>" + tempnet + "</td><td></td></tr>"

    # Comparacion EIGRP- redistribute
    tempnet = ""
    for net in rtemp.eigrp["redistribute"]:
        if not rconf.eigrp["redistribute"].__contains__(net):
            tempnet = tempnet + net + ", "
    if tempnet != "":
        resultado = resultado + "<tr><td> EIGRP redistribute </td><td>" + tempnet + "</td><td></td></tr>"

    # Comparacion OSPF
    tempnet = ""
    for net in rtemp.ospf["networks"]:
        if not rconf.ospf["networks"].__contains__(net):
            tempnet = tempnet + net + ", "
    if tempnet != "":
        resultado = resultado + "<tr><td> OSPF networks </td><td>" + tempnet + "</td><td></td></tr>"

    # Comparacion OSPF- redistribute
    tempnet = ""
    for net in rtemp.ospf["redistribute"]:
        if not rconf.ospf["redistribute"].__contains__(net):
            tempnet = tempnet + net + ", "
    if tempnet != "":
        resultado = resultado + "<tr><td> OSPF redistribute </td><td>" + tempnet + "</td><td></td></tr>"


    #SNMP configuration
    if rconf.snmp["user"] != rtemp.snmp["user"]:
        resultado = resultado + "<tr><td> SNMP user</td><td>" + rtemp.snmp["user"] + "</td>" \
                    "<td>" + rconf.snmp["user"] + "</td></tr>"

    if rconf.snmp["version"] != rtemp.snmp["version"]:
        resultado = resultado + "<tr><td> SNMP version</td><td>" + rtemp.snmp["version"] + "</td>" \
                    "<td>" + rconf.snmp["version"] + "</td></tr>"

    if rconf.snmp["host"] != rtemp.snmp["host"]:
        resultado = resultado + "<tr><td> SNMP host</td><td>" + rtemp.snmp["host"] + "</td>" \
                    "<td>" + rconf.snmp["host"] + "</td></tr>"

    #TFTP configuration
    if rconf.tftp["nvram"] != rtemp.tftp["nvram"]:
        resultado = resultado + "<tr><td> TFTP</td><td>" + rtemp.tftp["nvram"] + "</td>" \
                    "<td>" + rconf.tftp["nvram"] + "</td></tr>"

def verificar(router):
    confrouter = obtener_router_archivo('archivos/' + routers[router][0])
    x, num = router.split("R")
    temprouter = obtener_routers_template()[int(num)]

    return obtener_diferencias(confrouter, temprouter)



print(obtener_routers_template()[3])
print(obtener_router_archivo('config'))
