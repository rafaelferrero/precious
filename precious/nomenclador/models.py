from django.db import models
from django.utils.translation import ugettext_lazy as _


class Practica(models.Model):
    detalle = models.TextField(
        max_length=2000,
        verbose_name=_("Observaciones"),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Codigo(Practica):
    codigo = models.CharField(
        max_length=10,
        verbose_name=_("Código de Práctica")
    )
    nombre = models.CharField(
        max_length=255,
        verbose_name=_("Nombre"),
    )

    def __str__(self):
        return "{0} - {1}".format(
            self.codigo,
            self.nombre
        )


class Arancel(Practica):
    nombre = models.CharField(
        max_length=255,
        verbose_name=_("Nombre"),
    )

    def __str__(self):
        return "{0}".format(
            self.nombre
        )
