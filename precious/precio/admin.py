from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .models import (
    SolicitudAumento,
    Precio,
)


def autorizar(modeladmin, request, queryset):
    for obj in queryset:
        obj.aceptado = True
        obj.updater = request.user
        obj.save()
autorizar.short_description = _("Autorizar Solicitudes")


@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    pass


@admin.register(SolicitudAumento)
class SolicitudAumentoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'prestador',
                'vigencia_desde',
                'vigencia_hasta',
                'porcentaje_aumento',
                'aceptado',
            )
        }),
    )
    exclude = (
        'estado',
        'creator',
        'updater',
        'fecha_creacion',
        'fecha_modificacion',
    )
    list_display = (
        'prestador',
        'vigencia_desde',
        'vigencia_hasta',
        'porcentaje_aumento',
        'estado',
    )
    list_filter = (
        'prestador',
        'estado',
    )
    search_fields = (
        'prestador',
        'vigencia_desde',
        'vigencia_hasta',
    )
    actions = [autorizar]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'creator', None) is None:
            obj.creator = request.user
        obj.updater = request.user
        obj.save()
