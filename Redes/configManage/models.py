from django.db import models

# Create your models here.

class Reporte(models.Model):
    """
    Modelo que representa un reporte del sistema de tickets
    """
    ip = models.CharField(max_length=20,
                            help_text="IP del dispositivo donde se originó el reporte")

    descripcion = models.CharField(max_length=200,
                            help_text="Descripción del reporte")

    fecha = models.CharField(max_length=40,
                             help_text="Fecha de registro")


    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.ip + ":" + self.fecha + ":" + self.descripcion