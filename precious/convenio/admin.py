from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
import django_excel as excel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Prestador,
    Convenio,
    ArancelPractica,
    CodigoPractica,
    DetalleArancel,
    DetalleCodigo,
    Usuario,
    TipoPractica,
)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'usuarios'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


def export_homologacion(modeladmin, request, queryset):
    q = queryset.values(
        'codigo_prestador__tipo__tipo',
        'codigo_prestador__codigo',
        'codigo_prestador__nombre',
        'codigo_homologado__tipo__tipo',
        'codigo_homologado__codigo',
        'codigo_homologado__nombre')
    return excel.make_response_from_records(
        q,
        'xls',
        file_name="homologacion"
    )
export_homologacion.short_description = _("Exportar a homologacion a excel")


@admin.register(TipoPractica)
class TipoPracticaAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    search_fields = (
        'tipo',
        'prestador',
    )
    list_display = (
        'texto_completo',
    )
    list_filter = (
        'prestador',
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
            'fields': ('observacion',),
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
                'tipo',
                'codigo',
                'nombre',
                'prestador',
            )
        }),
        (_("Ampliar Detalles"), {
            'classes': ('collapse',),
            'fields': ('observacion',),
        })
    )
    list_display = (
        'tipo',
        'codigo',
        'nombre',
        'prestador',
    )
    list_filter = (
        'prestador',
        'tipo',
    )
    search_fields = (
        'codigo',
        'nombre',
        'observacion',
    )


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ('prestador', 'fecha_inicio',)
    search_fields = ('prestador',)
    date_hierarchy = 'fecha_inicio'


def get_nombre_prestador(request):
    u = User.objects.get(username=request.user)
    return u.usuario.prestador.nombre


@admin.register(DetalleArancel)
class DetalleArancelAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Como los aranceles no son tantos como los codigos dejo el select pero filtrados
        if db_field.name == "arancel_prestador":
            kwargs["queryset"] = ArancelPractica.objects.exclude(
                prestador__nombre=get_nombre_prestador(request))
        if db_field.name == "arancel_homologado":
            kwargs["queryset"] = ArancelPractica.objects.filter(
                prestador__nombre=get_nombre_prestador(request))
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
    actions = [export_homologacion]


@admin.register(DetalleCodigo)
class DetalleCodigoAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    # como son tantos los códigos se pone raw en vez del select por default
    raw_id_fields = (
        'codigo_prestador',
        'codigo_homologado',
    )
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
    actions = [export_homologacion]
