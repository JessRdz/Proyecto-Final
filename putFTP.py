import ftplib
import os

# Datos FTP
ftp_servidor = input('Servidor: ')
ftp_usuario = input('Usuario: ')
ftp_clave = input('Clave: ')
ftp_raiz = '/home/rcp'  # Carpeta del servidor donde queremos subir el fichero

# Datos del fichero a subir
fichero_origen = input('Nombre del archivo a cargar: ')  # Ruta al fichero que vamos a subir
fichero_destino = 'startup-config-Equipo8'  # Nombre que tendrá el fichero en el servidor

# Conectamos con el servidor
try:
    s = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
    print(s.getwelcome())
    try:
        f = open(fichero_origen, 'rb')
        s.storbinary('STOR ' + fichero_destino, f)
        s.quit()
    except:
        print("No se ha podido encontrar el fichero " + fichero_origen)
except:
    print("No se ha podido conectar al servidor " + ftp_servidor)