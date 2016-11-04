from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist,
    MultipleObjectsReturned,
)
from convenio.models import (
    Prestador,
    TipoPractica,
    CodigoPractica,
    DetalleCodigo,
)
import pyexcel as pe


class SubirExcel(models.Model):
    archivo = models.FileField()
    prestador = models.ForeignKey(Prestador)
    fila_titulo = models.BooleanField(
        default=True,
        verbose_name=_("La primer fila contiene los títulos de las columnas"),
    )
    columna_tipo = models.IntegerField(
        default=0,
        verbose_name=_("Columna de 'Tipo de Práctica'"),
        help_text=_("Aunque sea una columna vacía la misma debe existir.")
    )
    columna_codigo = models.IntegerField(
        default=1,
        verbose_name=_("Columna de 'Códigos de Prácticas'"),
    )
    columna_nombre = models.IntegerField(
        default=2,
        verbose_name=_("Columna de 'Nombres de las Prácticas'"),
    )
    columna_observaciones = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Columna de las 'Observaciones de las Prácticas'"),
    )

    def __str__(self):
        return "{0} - {1}".format(
            self.prestador,
            self.archivo,
        )

    class Meta:
        abstract = True


class ImportarPracticas(SubirExcel):
    creator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="ImportarPracticas_creador"
    )
    updater = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="ImportarPracticas_modificador",
    )

    def clen(self):
        if self.columna_tipo is None \
                or self.columna_tipo < 0:
            raise ValidationError(
                {'columna_tipo':
                 _("ERROR! Ud. NO ha indicado una columna de 'Tipo de Practica' "
                   "la cual es necesaria para la unicidad de prácticas")})

    def subir_codigos_prestador(self, records):
        for r in records:
            codigo = r[self.columna_codigo]
            nombre = r[self.columna_nombre]
            if self.columna_observaciones and len(r) > 2:
                obs = r[self.columna_observaciones]
            else:
                obs = ""

            t = None
            if self.columna_tipo is not None:
                try:
                    t, created = TipoPractica.objects.get_or_create(
                        tipo=r[self.columna_tipo],
                        prestador=self.prestador,
                    )
                except MultipleObjectsReturned:
                    print("Tipos de Prácticas repetidos encontrados para "
                          "un mismo prestador: {0}".format(r[self.columna_tipo]))
                    print(t)
                    t = TipoPractica.objects.filter(
                        tipo=r[self.columna_tipo],
                        prestador=self.prestador,
                    ).first()

            try:
                obj, created = CodigoPractica.objects.get_or_create(
                    prestador=self.prestador,
                    tipo=t,
                    codigo=codigo,
                    defaults={
                        'nombre': nombre,
                        'observacion': obs
                    },
                )
                if not created:
                    print("Error!! Código repetido {0}-{1}".format(codigo, nombre))
                    print(obj)
            except MultipleObjectsReturned:
                print("Códigos repetidos encontrados en un mismo prestador: {0}".format(codigo))

    def save(self, *args, **kwargs):
        super(ImportarPracticas, self).save(*args, **kwargs)
        records = iter(
            pe.get_sheet(
                file_name=self.archivo.path))

        if self.fila_titulo:
            next(records)

        self.subir_codigos_prestador(records)

    class Meta:
        verbose_name = _("Importar Prácticas en formato Excel (.xls)")
        verbose_name_plural = _("Importar Prácticas en formato Excel (.xls)")


class ImportarHomologacion(SubirExcel):
    columna_tipo_homologado = models.IntegerField(
        verbose_name=_("Columna de Tipo de Práctica Homologada"),
    )
    columna_codigo_homologado = models.IntegerField(
        verbose_name=_("Columna de Código de Práctica Homologada"),
    )
    creator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="ImportarHomologacion_creador"
    )
    updater = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="ImportarHomologacion_modificador",
    )

    def clean(self):
        if self.columna_tipo_homologado is None \
                or self.columna_tipo_homologado < 0:
            raise ValidationError(
                {'columna_tipo_homologado':
                    _("ERROR! Ud. a Indicado subir un archivo de "
                        "'Homologación de Códigos de Nomenclador' y no ha indicado cuál "
                        "es la 'Columna de Tipo de Práctica Homologada'")})
        if self.columna_codigo_homologado is None \
                or self.columna_codigo_homologado < 0:
            raise ValidationError(
                {'columna_codigo_homologado':
                    _("ERROR! Ud. a Indicado subir un archivo de "
                        "'Homologación de Códigos de Nomenclador' y no ha indicado cuál "
                        "es la 'Columna de Código Homologado'")})
        if self.columna_tipo is None \
                or self.columna_tipo < 0:
            raise ValidationError(
                {'columna_tipo':
                    _("ERROR! Ud. NO ha indicado una columna de 'Tipo de Practica' "
                      "la cual es necesaria para la unicidad de prácticas")})

    def subir_homologacion_codigos(self, records):
        for r in records:
            try:
                t = TipoPractica.objects.get(
                    tipo=r[self.columna_tipo],
                    prestador=self.prestador,
                )
            except ObjectDoesNotExist:
                raise ValidationError(
                    "ERROR! No se encuentra el tipo indicado: {0}".format(r[self.columna_tipo]))

            try:
                codigo = CodigoPractica.objects.get(
                    prestador=self.prestador,
                    codigo=r[self.columna_codigo],
                    tipo=t,
                )
            except ObjectDoesNotExist:
                print("ERROR! No se encuentra el Código indicado: {0}".format(r[self.columna_codigo]))
                codigo = None

            if r[self.columna_codigo_homologado] is not None \
                    and r[self.columna_codigo_homologado] != "":
                try:
                    t = TipoPractica.objects.get(
                        tipo=r[self.columna_tipo_homologado],
                        prestador=self.updater.usuario.prestador,
                    )
                except ObjectDoesNotExist:
                    raise ValidationError(
                        "ERROR! No se encuentra el tipo indicado: {0}".format(r[self.columna_tipo]))

                try:
                    homologado = CodigoPractica.objects.get(
                        prestador=self.updater.usuario.prestador,
                        codigo=r[self.columna_codigo_homologado],
                        tipo=t,
                    )
                except ObjectDoesNotExist:
                    print("Homologado: {0}".format(r[self.columna_codigo_homologado]))
            else:
                homologado = None

            if codigo:
                try:
                    obj, created = DetalleCodigo.objects.get_or_create(
                        convenio=self.prestador.convenio,
                        codigo_prestador=codigo,
                        codigo_homologado=homologado,
                    )
                    if not created:
                        print("Error!! Código repetido {0}-{1}".format(codigo, homologado))
                        print(obj)
                except MultipleObjectsReturned:
                    print("ERROR!! Códigos repetidos encontrados en un mismo convenio: {0}".format(codigo))

    def save(self, *args, **kwargs):
        super(ImportarHomologacion, self).save(*args, **kwargs)
        records = iter(
            pe.get_sheet(
                file_name=self.archivo.path))

        if self.fila_titulo:
            next(records)

        self.subir_homologacion_codigos(records)

    class Meta:
        verbose_name = _("Importar Homologación en formato Excel (.xls)")
        verbose_name_plural = _("Importar Homologación en formato Excel (.xls)")
