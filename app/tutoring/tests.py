from datetime import date  # Importa el módulo 'date' de 'datetime'

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from students.models import Estudiante
from .models import EntrevistaTutoria


class EntrevistaTutoriaViewTest(TestCase):
    def setUp(self):
        self.profesor = User.objects.create_user(
            username="profe1",
            password="12345678"
        )
        self.estudiante = Estudiante.objects.create(
            profesor=self.profesor,
            nombres="Ana",
            apellidos="Pérez",
            curso="5A",
            rut="11-1",
            activo=True,
        )

    def get_valid_data(self):
        return {
            "estudiante": self.estudiante.id,
            "fecha": str(date.today()),  # Usa 'date.today()' para obtener la fecha actual
            "situacion_trabajada": "Dificultades de organización escolar y participación en clases.",
            "fase_motivacional_dominante": "sin_identificar",
            "dimension_academica": "on",
            "dimension_socioemocional": "on",
            "desarrollo_sesion": "Se revisaron avances, obstáculos y posibles apoyos para la semana.",
            "meta_concreta": "Registrar tareas y materiales cada jornada.",
            "compromiso_tutor": "Monitorear avances y reforzar seguimiento.",
            "criterio_profesional": "continua_tutoria",
            "observaciones": "Se observa disposición positiva.",
        }

    def test_login_required_for_create_view(self):
        response = self.client.get(reverse("tutoring:create"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_access_create_view(self):
        self.client.login(username="profe1", password="12345678")
        response = self.client.get(reverse("tutoring:create"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_create_interview(self):
        self.client.login(username="profe1", password="12345678")
        response = self.client.post(
            reverse("tutoring:create"),
            data=self.get_valid_data(),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntrevistaTutoria.objects.count(), 1)

    def test_authenticated_user_can_edit_interview(self):
        entrevista = EntrevistaTutoria.objects.create(
            estudiante=self.estudiante,
            profesor=self.profesor,
            fecha=date.today(),
            situacion_trabajada="Situación breve válida.",
            fase_motivacional_dominante="sin_identificar",
            dimension_academica=True,
            desarrollo_sesion="Desarrollo breve válido.",
            meta_concreta="Meta breve válida.",
            compromiso_tutor="Compromiso breve válido.",
            criterio_profesional="continua_tutoria",
            observaciones="Observación breve.",
        )

        self.client.login(username="profe1", password="12345678")
        response = self.client.post(
            reverse("tutoring:update", kwargs={"pk": entrevista.id}),
            data=self.get_valid_data(),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        entrevista.refresh_from_db()
        self.assertEqual(entrevista.situacion_trabajada, "Dificultades de organización escolar y participación en clases.")

    def test_authenticated_user_can_delete_interview(self):
        entrevista = EntrevistaTutoria.objects.create(
            estudiante=self.estudiante,
            profesor=self.profesor,
            fecha=date.today(),
            situacion_trabajada="Situación breve válida.",
            fase_motivacional_dominante="sin_identificar",
            dimension_academica=True,
            desarrollo_sesion="Desarrollo breve válido.",
            meta_concreta="Meta breve válida.",
            compromiso_tutor="Compromiso breve válido.",
            criterio_profesional="continua_tutoria",
            observaciones="Observación breve.",
        )

        self.client.login(username="profe1", password="12345678")
        response = self.client.post(
            reverse("tutoring:delete", kwargs={"pk": entrevista.id}),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntrevistaTutoria.objects.count(), 0)