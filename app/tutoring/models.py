from django.contrib.auth.models import User
from django.db import models

from students.models import Estudiante


class EntrevistaTutoria(models.Model):
    FASE_MOTIVACIONAL_CHOICES = [
        ("sin_identificar", "Sin identificar"),
        ("precontemplacion", "Precontemplación"),
        ("contemplacion", "Contemplación"),
        ("preparacion", "Preparación"),
        ("accion", "Acción"),
        ("mantenimiento", "Mantenimiento"),
    ]

    CRITERIO_PROFESIONAL_CHOICES = [
        ("continua_tutoria", "Continúa tutoría"),
        ("mesa_de_casos", "Mesa de casos"),
        ("derivacion", "Derivación"),
    ]

    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        related_name="entrevistas_tutoria",
    )

    profesor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="entrevistas_tutoria",
    )

    fecha = models.DateField()

    situacion_trabajada = models.TextField()
    fase_motivacional_dominante = models.CharField(
        max_length=30,
        choices=FASE_MOTIVACIONAL_CHOICES,
        default="sin_identificar",
    )

    dimension_academica = models.BooleanField(default=False)
    dimension_socioemocional = models.BooleanField(default=False)
    dimension_identitaria = models.BooleanField(default=False)
    dimension_vincular = models.BooleanField(default=False)
    dimension_proyeccion = models.BooleanField(default=False)

    desarrollo_sesion = models.TextField(blank=True)
    meta_concreta = models.TextField()
    compromiso_tutor = models.TextField()

    criterio_profesional = models.CharField(
        max_length=30,
        choices=CRITERIO_PROFESIONAL_CHOICES,
    )

    observaciones = models.TextField(blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha", "-fecha_creacion"]

    def __str__(self):
        return f"{self.estudiante} - {self.fecha:%d/%m/%Y}"