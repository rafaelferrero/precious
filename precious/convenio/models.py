from django.db import models

from django.utils.translation import ugettext_lazy as _
from nomenclador.models import Arancel, Codigo


class Prestador(models.Model):
    nombre = models.CharField(
        max_length=255,
        verbose_name=_("Nombre del Prestador"),
    )

    def __str__(self):
        return "{0}".format(self.nombre)

    class Meta:
        ordering = ('nombre',)


class Convenio(models.Model):
    prestador = models.OneToOneField(
        Prestador,
        verbose_name=_("Prestador")
    )
    fecha_inicio = models.DateField(
        verbose_name=_("Fecha de inicio del convenio"),
    )

    def __str__(self):
        return "{0} ({1})".format(
            self.prestador,
            self.fecha_inicio
        )

    class Meta:
        ordering = ('prestador',)


class DetalleArancel(models.Model):
    convenio = models.ForeignKey(
        Convenio,
        verbose_name=_("Convenio"),
    )
    arancel_prestador = models.ForeignKey(
        Arancel,
        related_name='arancel_prestador',
        verbose_name=_("Arancel del Prestador"),
    )
    arancel_homologado = models.ForeignKey(
        Arancel,
        related_name='arancel_homologado',
        verbose_name=_("Arancel Homologado"),
    )

    class Meta:
        ordering = ('convenio', 'arancel_prestador',)

    def __str__(self):
        return "{0} - {1} homologa a {1}".format(
            self.convenio,
            self.arancel_prestador,
            self.arancel_homologado
        )


class DetalleCodigo(models.Model):
    convenio = models.ForeignKey(
        Convenio,
        verbose_name=_("Convenio"),
    )
    codigo_prestador = models.ForeignKey(
        Codigo,
        related_name='codigo_prestador',
        verbose_name=_("Código del Prestador"),
    )
    codigo_homologado = models.ForeignKey(
        Codigo,
        related_name='codigo_homologado',
        verbose_name=_("Código Homologado")
    )

    class Meta:
        ordering = ('convenio', 'codigo_prestador',)

    def __str__(self):
        return "{0} - {1} homologa a {1}".format(
            self.convenio,
            self.codigo_prestador,
            self.codigo_homologado
        )
