from django.db import models

# Create your models here.

class Estadistica(models.Model):
    """
        Modelo que representa un flujo de NetFlow
    """

    fecha = models.DateTimeField(max_length=40,
                                 help_text="Fecha de registro")

    ip = models.CharField(max_length=20,
                                 help_text="IP del dispositivo origen")

    tipo = models.CharField(max_length=20,
                                help_text="Tipo de estadística")

    valor = models.CharField(max_length=10,
                               help_text="Valor de la estadística")


    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return str(self.fecha) + ":" + str(self.ip) + ":" + str(self.tipo) + ":" + str(self.valor)