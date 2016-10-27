from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from .models import (
    Prestador,
    Convenio,
    ArancelPractica,
    CodigoPractica,
    DetalleArancel,
    DetalleCodigo,
)


@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(ArancelPractica)
class ArancelPracticaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'nombre',
                'prestador',
            )
        }),
        (_("Ampliar Detalles"), {
            'classes': ('collapse',),
            'fields': ('detalle',),
        })
    )
    list_display = (
        'nombre',
        'prestador',
    )
    list_filter = (
        'prestador',
    )
    search_fields = (
        'nombre',
        'prestador',
        'descripcion',
    )


@admin.register(CodigoPractica)
class CodigoPracticaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'codigo',
                'nombre',
                'prestador',
            )
        }),
        (_("Ampliar Detalles"), {
            'classes': ('collapse',),
            'fields': ('detalle',),
        })
    )
    list_display = (
        'codigo',
        'nombre',
        'prestador',
    )
    list_filter = (
        'prestador',
    )
    search_fields = (
        'codigo',
        'nombre',
        'descripcion',
    )


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ('prestador', 'fecha_inicio',)
    search_fields = ('prestador',)
    date_hierarchy = 'fecha_inicio'


@admin.register(DetalleArancel)
class DetalleArancelAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "arancel_prestador":
            kwargs["queryset"] = ArancelPractica.objects.exclude(prestador__nombre="GECROS")
        if db_field.name == "arancel_homologado":
            kwargs["queryset"] = ArancelPractica.objects.filter(prestador__nombre="GECROS")
        return super(DetalleArancelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'convenio',
                'arancel_prestador',
                'arancel_homologado',
            )
        }),
    )
    list_display = (
        'convenio',
        'arancel_prestador',
        'arancel_homologado',
    )
    search_fields = (
        'convenio',
        'arancel_prestador',
        'arancel_homologado',
    )
    list_filter = (
        'convenio',
    )


@admin.register(DetalleCodigo)
class DetalleCodigoAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "codigo_prestador":
            kwargs["queryset"] = CodigoPractica.objects.exclude(prestador__nombre="GECROS")
        if db_field.name == "codigo_homologado":
            kwargs["queryset"] = CodigoPractica.objects.filter(prestador__nombre="GECROS")
        return super(DetalleCodigoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'convenio',
                'codigo_prestador',
                'codigo_homologado',
            )
        }),
    )
    list_display = (
        'convenio',
        'codigo_prestador',
        'codigo_homologado',
    )
    search_fields = (
        'convenio',
        'codigo_prestador',
        'codigo_homologado',
    )
    list_filter = (
        'convenio',
    )
