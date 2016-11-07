from django.contrib import admin
from .models import (
    ImportarPracticas,
    ImportarHomologacion,
    ErrorImportacionPractica,
    ErrorImportacionHomologacion,
)


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
