from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Arancel, Codigo


@admin.register(Arancel)
class ArancelAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'nombre',
            )
        }),
        (_("Ampliar Detalles"), {
            'classes': ('collapse',),
            'fields': ('detalle',),
        })
    )
    list_display = (
        'nombre',
    )
    search_fields = (
        'nombre',
        'descripcion',
    )


@admin.register(Codigo)
class CodigoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fieldsets = (
        (None, {
            'fields': (
                'codigo',
                'nombre',
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
    )
    search_fields = (
        'codigo',
        'nombre',
        'descripcion',
    )
