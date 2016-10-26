from django.contrib import admin
from .models import Prestador, Convenio, DetalleArancel, DetalleCodigo


@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ('prestador', 'fecha_inicio',)
    search_fields = ('prestador',)
    date_hierarchy = 'fecha_inicio'


@admin.register(DetalleArancel)
class DetalleArancelAdmin(admin.ModelAdmin):
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
