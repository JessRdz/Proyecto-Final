import os
import re

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


print(obtener_routers_template()[3])
print(obtener_router_archivo('config'))
