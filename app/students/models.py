from django.contrib.auth.models import User
from django.db import models


class Estudiante(models.Model):
    profesor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="estudiantes",
    )
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    rut = models.CharField(max_length=20, blank=True)
    curso = models.CharField(max_length=50)
    correo_apoderado = models.EmailField(blank=True)
    telefono_apoderado = models.CharField(max_length=20, blank=True)
    observaciones = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ["curso", "apellidos", "nombres"]

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.curso}"


class RegistroImportacion(models.Model):
    profesor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="importaciones",
    )
    nombre_archivo = models.CharField(max_length=255)
    total_registros = models.PositiveIntegerField(default=0)
    registros_exitosos = models.PositiveIntegerField(default=0)
    registros_error = models.PositiveIntegerField(default=0)
    fecha_importacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Importación"
        verbose_name_plural = "Registros de Importación"
        ordering = ["-fecha_importacion"]

    def __str__(self):
        return f"{self.nombre_archivo} - {self.fecha_importacion:%d/%m/%Y %H:%M}"