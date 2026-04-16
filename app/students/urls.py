from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.student_list, name="list"),
    path("nuevo/", views.student_create, name="create"),
    path("importar-csv/", views.student_import_csv, name="import_csv"),
    path("editar/<int:pk>/", views.student_update, name="update"),
    path("eliminar/<int:pk>/", views.student_delete, name="delete"),
]