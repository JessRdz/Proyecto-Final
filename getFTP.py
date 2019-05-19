import ftplib
import os

# Datos FTP
ftp_servidor = input('Servidor: ')
ftp_usuario = input('Usuario: ')
ftp_clave = input('Clave: ')

# Datos del fichero a subir
fichero_origen = 'startup-config'  # Ruta al fichero que vamos a subir
fichero_destino = input('Nombre con el que se guardará el archivo: ')  # Nombre que tendrá el fichero en el servidor

# Conectamos con el servidor
try:
    s = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
    print(s.getwelcome())
    try:
        f = open(fichero_destino, 'wb')
        s.retrbinary('RETR ' + fichero_origen, f.write)
        s.quit()
    except:
        print("No se ha podido encontrar el fichero " + fichero_origen)
except:
    print("No se ha podido conectar al servidor " + ftp_servidor)