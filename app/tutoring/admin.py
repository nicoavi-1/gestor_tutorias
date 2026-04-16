from django.contrib import admin
from django.contrib.auth.models import Group

from .models import EntrevistaTutoria


# Crear un filtro para limitar las tutorías del profesor actual
class EntrevistaTutoriaAdmin(admin.ModelAdmin):
    list_display = ("estudiante", "profesor", "fecha", "criterio_profesional")
    list_filter = ("profesor",)
    search_fields = ("estudiante__nombres", "profesor__username", "fecha")
    
    def get_queryset(self, request):
        """Limitar los registros a los del profesor logueado."""
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(profesor=request.user)

admin.site.register(EntrevistaTutoria, EntrevistaTutoriaAdmin)