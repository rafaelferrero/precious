from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
# from django.db.models import Q
from precious.precious.convenio.models import (
    Prestador,
    Detalle,
)


class SolicitudAumento(models.Model):
    ESTADOS = (
        ('P', _("Propuesto")),
        ('R', _("Renegociado")),
        ('C', _("Conforme")),
        ('A', _("Autorizado")),
    )

    vigencia_desde = models.DateField(
        default=datetime.today(),
    )
    vigencia_hasta = models.DateField(
        null=True,
        blank=True,
    )
    porcentaje_aumento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    # OCULTOS
    estado = models.CharField(
        max_length=1,
        choices=ESTADOS,
        default=ESTADOS[0][0],
    )
    aceptado = models.BooleanField(
        default=False,
    )
    creator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="solicitud_creador",
    )
    updater = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="solicitud_modificador",
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
    )

    # TODO: hacer el clean, porcentaje no puede ser mayor a 100,00
    #   Tambien se debe controlar que no exista una solicitud repetida
    #   para el prestador en un mismo periodo de tiempo.

    def cambio_estado(self):
        if self.pk:
            if self.creator == self.updater:
                if self.aceptado:
                    rta = 'C'
                else:
                    rta = 'P'
            else:
                if self.aceptado:
                    rta = 'A'
                else:
                    rta = 'R'
        else:
            rta = 'P'
        return rta

    def save(self, *args, **kwargs):
        super(SolicitudAumento, self).save(*args, **kwargs)
        self.estado = self.cambio_estado()
        if self.estado == 'A':
            print("ahora hay que ponerle los precios a los codigos")

    @property
    def solicitud(self):
        if autorizada:
            estado = "Autorizada"
        else:
            estado = "Pendiente de aprobación"
        return "Solicitud Nro. {0} {1} de {2}".format(
            self.pk,
            estado,
            not self.prestador.nombre
        )

    @property
    def vigencia(self):
        if self.vigencia_hasta:
            vigencia = "{0} a {1}".format(
                self.vigencia_desde,
                self.vigencia_hasta,
            )
        else:
            vigencia = "vigente desde {0}".format(
                self.vigencia_desde,
            )
        return vigencia

    def __str__(self):
        return "{0} - Aumento {1}% desde el {2}".format(
            self.solicitud,
            self.porcentaje,
            self.vigencia,
        )


class Precio(models.Model):
    detalle = models.ForeignKey(
        Detalle,
    )
    solicitud = models.ForeignKey(
        SolicitudAumento
    )
    importe = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        default=0,
    )

    @property
    def __str__(self):
        return "${0} (vigencia: {1})".format(
            self.importe,
            self.solicitud.vigencia,
        )

    # TODO: Importe vigente en funcion del detalle
    # TODO: Importe vigente en funcion de la fecha y el detalle
