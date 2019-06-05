import Puller as pull
import requests
import time


def nuevo_reporte(request, ip, descripcion):
    requests.get("http://127.0.0.1:8000/configManage/reportes/" + ip +
                 "/" + descripcion + "/" + time.strftime("%c"))


f = open("dispositivos", 'w')
dispositivos = pull.conocer_red()
conexiones = pull.cadena(dispositivos)
f.write(conexiones)
f.close()

while True:
    dispositivos = pull.ping_dispositivos(dispositivos)
    conexiones = pull.cadena(dispositivos)
    pull.mostrar(dispositivos)
    f = open("dispositivos", 'w')
    f.write(conexiones)
    f.close()

    time.sleep(2)
