from django.db import models
from django.utils.translation import ugettext_lazy as _


class Prestador(models.Model):
    nombre = models.CharField(
        max_length=255,
        verbose_name=_("Nombre del Prestador"),
    )

    def __str__(self):
        return "{0}".format(self.nombre)

    class Meta:
        ordering = ('nombre',)
        verbose_name = _("Prestador")
        verbose_name_plural = _("Prestadores")


class Practica(models.Model):
    prestador = models.ForeignKey(Prestador)
    detalle = models.TextField(
        max_length=2000,
        verbose_name=_("Observaciones"),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ('prestador',)
        verbose_name = _("Práctica")
        verbose_name_plural = _("Prácticas")


class CodigoPractica(Practica):
    codigo = models.CharField(
        max_length=10,
        verbose_name=_("Código de Práctica")
    )
    nombre = models.CharField(
        max_length=255,
        verbose_name=_("Nombre"),
    )

    def __str__(self):
        return "{0} - {1} - {2}".format(
            self.codigo,
            self.nombre,
            self.prestador,
        )

    class Meta:
        ordering = ('codigo', 'prestador',)
        verbose_name = _("Código de Práctica")
        verbose_name_plural = _("Códigos de Prácticas")


class ArancelPractica(Practica):
    nombre = models.CharField(
        max_length=255,
        verbose_name=_("Nombre"),
    )

    def __str__(self):
        return "{0} - {1}".format(
            self.nombre,
            self.prestador,
        )

    class Meta:
        verbose_name = _("Arancel de Práctica")
        verbose_name_plural = _("Aranceles de Prácticas")


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
        verbose_name = _("Convenio con Prestador")
        verbose_name_plural = _("Convenios con Prestadores")


class Detalle(models.Model):
    convenio = models.ForeignKey(
        Convenio,
        verbose_name=_("Convenio"),
    )

    class Meta:
        abstract = True
        ordering = ('convenio',)


class DetalleArancel(Detalle):
    arancel_prestador = models.ForeignKey(
        ArancelPractica,
        related_name='arancel_prestador',
        verbose_name=_("Arancel del Prestador"),
    )
    arancel_homologado = models.ForeignKey(
        ArancelPractica,
        blank=True,
        null=True,
        related_name='arancel_homologado',
        verbose_name=_("Arancel Homologado"),
    )

    class Meta:
        ordering = ('convenio', 'arancel_prestador',)
        verbose_name = _("Detalle de Convenio de Aranceles de Práctica")
        verbose_name_plural = _("Detalles de Convenio de Aranceles de Práctica")

    def __str__(self):
        return "{0} - {1} homologa a {1}".format(
            self.convenio,
            self.arancel_prestador,
            self.arancel_homologado
        )


class DetalleCodigo(Detalle):
    codigo_prestador = models.ForeignKey(
        CodigoPractica,
        related_name='codigo_prestador',
        verbose_name=_("Código del Prestador"),
    )
    codigo_homologado = models.ForeignKey(
        CodigoPractica,
        blank=True,
        null=True,
        related_name='codigo_homologado',
        verbose_name=_("Código Homologado")
    )

    class Meta:
        ordering = ('convenio', 'codigo_prestador',)
        verbose_name = _("Detalle de Convenio de Códigos de Práctica")
        verbose_name_plural = _("Detalles de Convenio de Códigos de Práctica")

    def __str__(self):
        return "{0} - {1} homologa a {1}".format(
            self.convenio,
            self.codigo_prestador,
            self.codigo_homologado
        )
