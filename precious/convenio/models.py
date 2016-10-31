from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import pyexcel as pe
import pdb


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
        # unique_together = ('codigo', 'prestador',)
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


class Usuario(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    prestador = models.ForeignKey(Prestador)


class SubirExcelCodigos(models.Model):
    TIPOS_ARCHIVO = (
        ('C', _("Códigos de Nomenclador del Prestador")),
        ('H', _("Homologación de Códigos de Nomenclador")),
    )
    archivo = models.FileField()
    tipo_archivo = models.CharField(
        max_length=15,
        verbose_name=_("Tipo de Archivo"),
        choices=TIPOS_ARCHIVO,
        default=TIPOS_ARCHIVO[0][0]
    )
    prestador = models.ForeignKey(Prestador)
    fila_titulo = models.BooleanField(
        default=True,
        verbose_name=_("La primer fila contiene los títulos de las columnas"),
    )
    columna_codigo = models.IntegerField(
        default=0,
        verbose_name=_("Columna de Códigos de Nomenclador del Prestador"),
    )
    columna_nombre = models.IntegerField(
        default=1,
        verbose_name=_("Columna de nombres de los Códigos de Nomenclador"),
    )
    columna_detalle = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Columna de Detalles de los Códigos de Nomenclador"),
    )
    columna_codigo_homologado = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Columna de Código Homologado"),
    )

    class Meta:
        verbose_name = _("Subir archivo en formato Excel (.xls)")
        verbose_name_plural = _("Subir archivos en formato Excel (.xls)")

    def __str__(self):
        return "{0} - {1}".format(
            self.prestador,
            self.archivo,
        )

    def clean(self):
        # pdb.set_trace()
        if self.tipo_archivo == 'H':
            if self.columna_codigo_homologado is None \
                    or self.columna_codigo_homologado < 0:
                raise ValidationError(
                    {'columna_codigo_homologado':
                        _("ERROR! Ud. a Indicado subir un archivo de "
                            "'Homologación de Códigos de Nomenclador' y no ha indicado cuál "
                            "es la 'Columna de Código Homologado'")})

    def subir_codigos_prestador(self, records):
        for r in records:
            codigo = r[self.columna_codigo]
            nombre = r[self.columna_nombre]

            if self.columna_detalle and len(r) > 2:
                detalle = r[self.columna_detalle]
            else:
                detalle = ""

            obj, created = CodigoPractica.objects.get_or_create(
                prestador=self.prestador,
                codigo=codigo,
                nombre=nombre,
                detalle=detalle)

            if not created:
                print(obj)

    def subir_homologacion_codigos(self, records):
        for r in records:
            # pdb.set_trace()
            codigo = r[self.columna_codigo]
            homologado = r[self.columna_codigo_homologado]

            obj, created = DetalleCodigo.objects.get_or_create(
                convenio=self.prestador.convenio,
                codigo_prestador=codigo,
                codigo_homologado=homologado,
                )

            if not created:
                print(obj)

    def save(self, *args, **kwargs):
        super(SubirExcelCodigos, self).save(*args, **kwargs)
        records = iter(
            pe.get_sheet(
                file_name=self.archivo.path))

        if self.fila_titulo:
            next(records)

        if self.tipo_archivo == 'C':
            self.subir_codigos_prestador(records)
        elif self.tipo_archivo == 'H':
            self.subir_homologacion_codigos(records)
