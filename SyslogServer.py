LOG_FILE = 'log.log'
HOST, PORT = "50.0.0.2", 2000
import logging
import socketserver
from Email import send_notification
from sms import sendSms, countLines, checkLevelNot
import subprocess

niveles = ["Emergencia", "Alerta", "Critico", "Error", "Advertencia", "Notificacion", "Informacion", "Debugging"]

logging.basicConfig(level=logging.DEBUG, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

#Obtiene el nivel del mensaje (0 a 7 )
def obtenerNivel(mensaje_syslog):
    inicio = mensaje_syslog.find("<") + 1
    fin = mensaje_syslog.find(">")
    nivel = int(mensaje_syslog[inicio:fin]) % 8
    fechaini = mensaje_syslog.find("*")
    fechafin = fechaini + 19
    fecha = mensaje_syslog[fechaini:fechafin]
    descripcion = mensaje_syslog.split(":")[5]

    return niveles[nivel] + ": " + fecha + ":" + descripcion

#Notifica por sistema
def notificar_sistema(mensaje):
    command = ['notify-send', mensaje]
    subprocess.call(command, stdout=False)

#Manda notificaciones por correo, sms y notifica por sistema
def notificar(mensaje_syslog, ip):
    mensaje = ip + obtenerNivel(mensaje_syslog)
    notificar_sistema(mensaje)
    if countLines() % 1 == 0:
        checkLevelNot()
        with open('NotifyNews.txt', 'r') as myfile:
            data = myfile.read()
            with open('log.log', 'r') as myfile2:
                data2 = myfile2.read()
            sendSms(mensaje)
            send_notification("alaidleonz@gmail.com", "Nuevas Alertas", mensaje)



#Comportamiento del servidor UDP que recibira los logs
class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        logging.debug(str(self.client_address[0]) + ": " + obtenerNivel(str(data)))
        socket = self.request[1]
        print( str(self.client_address[0]) + ": " + obtenerNivel(str(data)))
        notificar(str(data), self.client_address[0])



if __name__ == "__main__":
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")