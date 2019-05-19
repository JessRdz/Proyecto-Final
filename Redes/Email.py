from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_notification(to, subject, message):

    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = "redes2019"
    msg['From'] = "redes.notificaciones.python@gmail.com"
    msg['To'] = to
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print("Correo enviado a %s correctamente." % (msg['To']))