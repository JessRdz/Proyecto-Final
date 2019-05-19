from django.db import models

# Create your models here.

class Flow(models.Model):
    """
        Modelo que representa un flujo de NetFlow
    """

    fecha = models.DateTimeField(max_length=40,
                                 help_text="Fecha de registro")

    servicio = models.CharField(max_length=20,
                                help_text="Servicio")

    size = models.IntegerField(max_length=10,
                               help_text="Tamaño en bytes del flujo")

    duration = models.IntegerField(max_length=10,
                               help_text="Tamaño en bytes del flujo")

    ip_origen = models.CharField(max_length=20,
                                 help_text="IP del dispositivo origen")

    ip_destino = models.CharField(max_length=20,
                                 help_text="IP del dispositivo destino")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return str(self.fecha) + ":" + self.servicio + ":" + str(self.size) + ":" + str(self.duration) + ":" + self.ip_origen + " to " + self.ip_destino