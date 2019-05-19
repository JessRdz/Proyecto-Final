import tftpy
import os.path as path
import os
import filecmp
import shutil
import threading
import Puller
import time
from SNMPget import getSNMP

ips = Puller.conocer_red()
ips.remove(["50.0.0.2", 0])
inventario = {}
directorio = "archivos/"
mibSysdesc = "1.3.6.1.2.1.1.1.0"
chasisId = "1.3.6.1.4.1.9.3.6.3.0"
mib = {"1.3.6.1.4.1.9.3.6.11.1.3",
       "1.3.6.1.4.1.9.3.6.11.1.4"}
#1.3.6.1.4.1.9.3.6.11 card table
#1.3.6.1.4.1.9.3.6.11.1 card table entry
#1.3.6.1.4.1.9.3.6.11.1.3 card des
#1.3.6.1.4.1.9.3.6.11.1.4 card serial
#1.3.6.1.4.1.9.3.6.3 chassis id

def obtenerConfiguraciones():
    while 1:
        for router, bandera in ips:
            try:
                if path.exists(directorio + router):
                    tftpy.TftpClient(router, 69).download('startup-config', directorio + router + "-temp")
                    f = open(directorio + router)
                    ftemp = open(directorio + router + "-temp")
                    filecmp.clear_cache()
                    if not f.readlines() == ftemp.readlines():  # Regresa true si son iguales
                        print("Cambios detectados en el archivo de: " + router)
                        shutil.move( directorio + router + "-temp", directorio + router)
                    else:
                        os.remove(directorio + router + "-temp")
                    f.close()

                else:
                    tftpy.TftpClient(router, 69).download('startup-config', directorio + router)

            except:
                print("Falló la comunicación con " + router + "...")

        print("Archivos obtenidos")
        time.sleep(20)

def obtenerInventario():
    print("Obteniendo inventario:")
    resultado = []
    for ip, b in ips:
        print(ip + ":")
        x, sysDesc = getSNMP(ip, "demo", "password", mibSysdesc).split("=")
        sysDesc = sysDesc + "\nModulos:"
        for i in range(1, 6):
            modulo = "\n"
            for m in mib:
                card = getSNMP(ip, "demo", "password", m + "." + str(i))
                if card != "ERROR":
                    mi, cont = card.split("=")
                    modulo = modulo + cont + "  "
            if modulo != "\n":
                sysDesc = sysDesc + modulo
        resultado.append([ip, sysDesc])
    return resultado

def mostrarInventario(inventario):
    f = open("inventario", mode="w")
    resultado = ""
    for ip, descr in inventario:
        resultado = resultado + "\n" + ip + ":\n" + descr + "\n"
        f.write("\n" + ip + ":\n" + descr + "\n")
        print("\n" + ip + ":\n" + descr + "\n")

    return resultado


#mostrarInventario(obtenerInventario())
obtenerConfiguraciones()