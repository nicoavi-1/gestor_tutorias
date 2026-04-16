from django.contrib import admin

from .models import Estudiante, RegistroImportacion


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = (
        "nombres",
        "apellidos",
        "curso",
        "profesor",
        "activo",
    )
    search_fields = (
        "nombres",
        "apellidos",
        "rut",
        "curso",
    )
    list_filter = (
        "curso",
        "activo",
    )


@admin.register(RegistroImportacion)
class RegistroImportacionAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_archivo",
        "profesor",
        "total_registros",
        "registros_exitosos",
        "registros_error",
        "fecha_importacion",
    )
    list_filter = ("fecha_importacion",)
    search_fields = ("nombre_archivo", "profesor__username")