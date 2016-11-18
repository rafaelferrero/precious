from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
import django_excel as excel
from .models import (
    ImportarPracticas,
    ImportarHomologacion,
    ErrorImportacionPractica,
    ErrorImportacionHomologacion,
)


def export_data(modeladmin, request, queryset):
    return excel.make_response_from_query_sets(
        queryset,
        modeladmin.list_display,
        'xls',
        file_name="errores"
    )
export_data.short_description = _("Exportar a excel")


@admin.register(ErrorImportacionPractica)
class ErrorImportacionPracticaAdmin(admin.ModelAdmin):
    list_display = (
        'mensaje_error',
        'tipo_practica',
        'codigo_practica',
        'nombre_practica',
        'obs_practica',
        'prestador',
    )
    list_filter = (
        'prestador',
    )
    actions = [export_data]


@admin.register(ErrorImportacionHomologacion)
class ErrorImportacionHomologacionAdmin(admin.ModelAdmin):
    list_display = (
        'mensaje_error',
        'tipo_practica',
        'codigo_practica',
        'nombre_practica',
        'obs_practica',
        'tipo_homologado',
        'codigo_homologado',
        'convenio',
    )
    list_filter = (
        'convenio',
    )
    actions = [export_data]


@admin.register(ImportarPracticas)
class ImportarPracticasAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = (
        'archivo',
        'prestador',
    )
    exclude = ('creator', 'updater')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'creator', None) is None:
            obj.creator = request.user
        obj.updater = request.user
        obj.save()


@admin.register(ImportarHomologacion)
class ImportarHomologacionAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = (
        'archivo',
        'convenio',
    )
    exclude = ('creator', 'updater')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'creator', None) is None:
            obj.creator = request.user
        obj.updater = request.user
        obj.save()
