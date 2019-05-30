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

print(obtener_routers_template()[0])