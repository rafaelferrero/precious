from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Q
from convenio.models import (
    Prestador,
    Detalle,
)
from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist,
)


class SolicitudAumento(models.Model):
    ESTADOS = (
        ('P', _("Propuesto")),
        ('R', _("Renegociado")),
        ('C', _("Conforme")),
        ('A', _("Autorizado")),
    )

    vigencia_desde = models.DateField(
        default=timezone.now,
    )
    vigencia_hasta = models.DateField(
        null=True,
        blank=True,
    )
    porcentaje_aumento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    aceptado = models.BooleanField(
        default=False,
    )
    # OCULTOS
    prestador = models.ForeignKey(
        Prestador,
        null=True,
        blank=True,
    )
    estado = models.CharField(
        max_length=1,
        choices=ESTADOS,
        default=ESTADOS[0][0],
    )
    creator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="solicitud_creador",
    )
    updater = models.ForeignKey(
        User,
        blank=True,
        null=True,
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
    @property
    def solicitud(self):
        if self.estado == 'A':
            estado = "Autorizada"
        else:
            estado = "Pendiente de aprobación"
        return "Solicitud Nro. {0} {1} de {2}".format(
            self.pk,
            estado,
            self.prestador,
        )

    @property
    def vigencia(self):
        vigencia = "vigente desde "
        if self.vigencia_hasta:
            vigencia += "{0} a {1}".format(
                self.vigencia_desde,
                self.vigencia_hasta,
            )
        else:
            vigencia += "{0}".format(
                self.vigencia_desde,
            )
        return vigencia

    def cambio_estado(self):
        if self.creator.is_staff and self.aceptado and \
                self.creator.usuario.prestador.nombre == "Gecros":
            rta = 'A'
        elif self.pk:
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

    def clean(self):
        solicitud = SolicitudAumento.objects.filter(prestador=self.prestador)
        solicitud = solicitud.filter(vigencia_desde__gte=self.vigencia_desde)
        solicitud = solicitud.count()
        if solicitud > 0:
            raise ValidationError(
                {'vigencia_desde':
                 _("Ya existe una solicitud con fecha mayor a la indicada")})

    def cierre_vigencia(self):
        solicitudes = SolicitudAumento.objects.filter(
            prestador=self.prestador,
            vigencia_desde__lt=self.vigencia_desde,
            vigencia_hasta__isnull=True,
            estado="A",
        )
        if solicitudes:
            solicitudes.update(vigencia_hasta=self.vigencia_desde)

    def save(self, *args, **kwargs):
        self.estado = self.cambio_estado()
        if self.prestador is None:
            self.prestador = self.creator.usuario.prestador
        if self.estado == 'A':
            self.cierre_vigencia()
        super(SolicitudAumento, self).save(*args, **kwargs)

    def __str__(self):
        return "{0} - Aumento {1}% - {2}".format(
            self.solicitud,
            self.porcentaje_aumento,
            self.vigencia,
        )

    class Meta:
        verbose_name = _("Solicitud de Aumento")
        verbose_name_plural = _("Solicitudes de Aumento")


class Precio(models.Model):
    detalle = models.ForeignKey(
        Detalle,
    )
    solicitud = models.ForeignKey(
        SolicitudAumento,
    )
    importe = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        default=0,
    )

    class Meta:
        unique_together = (('detalle', 'solicitud'),)

    def __str__(self):
        return "{0} ${1} (vigencia: {2})".format(
            self.detalle,
            self.importe,
            self.solicitud.vigencia,
        )

    @receiver(post_save, sender=SolicitudAumento)
    def ejecutar_aumento(sender, **kwargs):
        if kwargs.get('created', False):
            convenio = Detalle.objects.filter(
                convenio__prestador=kwargs['instance'].prestador)
            ultima_solicitud = SolicitudAumento.objects.filter(
                vigencia_hasta__isnull=False,
                prestador=kwargs['instance'].prestador,
            ).order_by('-vigencia_hasta')[0:1]
            for codigo in convenio:
                try:
                    precio_anterior = Precio.objects.get(
                        solicitud=ultima_solicitud,
                        detalle=codigo,
                    )
                except ObjectDoesNotExist:
                    print("El codigo {0} no estaba valorizado, hacer a mano".format(
                        codigo
                    ))
                    precio_anterior = None

                if precio_anterior:
                    Precio.objects.create(
                        solicitud=kwargs['instance'],
                        detalle=codigo,
                        importe=precio_anterior.importe * (1 + kwargs['instance'].porcentaje_aumento / 100)
                    )

    # TODO: Importe vigente en funcion del detalle
    # TODO: Importe vigente en funcion de la fecha y el detalle
