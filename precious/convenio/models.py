from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


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
    observacion = models.TextField(
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


class TipoPractica(models.Model):
    tipo = models.CharField(
        max_length=255,
        verbose_name=_("Tipo de Práctica"),
        null=True,
        blank=True,
    )
    prestador = models.ForeignKey(Prestador)

    @property
    def solo_nombre(self):
        if self.tipo:
            return self.tipo
        else:
            return "[Sin Tipo]"

    @property
    def texto_completo(self):
        if self.tipo:
            texto = _("{0} - {1}").format(
                self.tipo,
                self.prestador,
            )
        else:
            texto = _("[Sin Tipo] - {0}").format(
                self.prestador,
            )
        return texto

    def __str__(self):
        return self.solo_nombre

    class Meta:
        unique_together = ('tipo', 'prestador',)
        verbose_name = _("Tipo de Práctica")
        verbose_name_plural = _("Tipos de Prácticas")


class CodigoPractica(Practica):
    tipo = models.ForeignKey(
        TipoPractica,
        null=True,
        blank=True,
        verbose_name=_("Tipo de Práctica")
    )
    codigo = models.CharField(
        max_length=10,
        verbose_name=_("Código de Práctica")
    )
    nombre = models.CharField(
        max_length=255,
        verbose_name=_("Nombre"),
    )

    def __str__(self):
        return "{0} - {1} - {2} - {3}".format(
            self.tipo,
            self.codigo,
            self.nombre,
            self.prestador,
        )

    class Meta:
        ordering = ('codigo', 'prestador',)
        unique_together = ('tipo', 'codigo', 'prestador',)
        verbose_name = _("Código de Práctica")
        verbose_name_plural = _("Códigos de Prácticas")


class ArancelPractica(Practica):
    nombre = models.CharField(
        max_length=255,
        verbose_name=_("Nombre"),
    )

    def __str__(self):
        return self.nombre

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
        # abstract = True
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

    def __str__(self):
        return "{0} - {1} homologa a {1}".format(
            self.convenio,
            self.arancel_prestador,
            self.arancel_homologado
        )

    class Meta:
        ordering = ('convenio', 'arancel_prestador',)
        verbose_name = _("Detalle de Convenio de Aranceles de Práctica")
        verbose_name_plural = _("Detalles de Convenio de Aranceles de Práctica")


class DetalleCodigo(Detalle):
    codigo_prestador = models.ForeignKey(
        CodigoPractica,
        related_name='codigo_prestador',
        verbose_name=_("Código del Prestador"),
    )
    codigo_homologado = models.ForeignKey(
        CodigoPractica,
        default=None,
        blank=True,
        null=True,
        related_name='codigo_homologado',
        verbose_name=_("Código Homologado")
    )

    def __str__(self):
        return "{0} - {1} homologa a {1}".format(
            self.convenio,
            self.codigo_prestador,
            self.codigo_homologado
        )

    class Meta:
        ordering = ('convenio', 'codigo_prestador',)
        verbose_name = _("Detalle de Convenio de Códigos de Práctica")
        verbose_name_plural = _("Detalles de Convenio de Códigos de Práctica")


class Usuario(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    prestador = models.ForeignKey(Prestador)


