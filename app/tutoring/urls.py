from django.urls import path

from . import views

app_name = "tutoring"

urlpatterns = [
    path("nuevo/", views.interview_create, name="create"),
    path("estudiante/<int:student_id>/", views.interview_list, name="list"),
    path("editar/<int:pk>/", views.interview_update, name="update"),
    path("eliminar/<int:pk>/", views.interview_delete, name="delete"),
]