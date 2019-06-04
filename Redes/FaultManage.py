import Puller as pull
import requests
import time


def nuevo_reporte(request, ip, descripcion):
    requests.get("http://127.0.0.1:8000/configManage/reportes/" + ip +
                 "/" + descripcion + "/" + time.strftime("%c"))


f = open("dispositivos")
f.write()