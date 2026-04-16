import csv
import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CSVImportForm, EstudianteForm
from .models import Estudiante, RegistroImportacion


@login_required
def student_list(request):
    estudiantes = Estudiante.objects.filter(
        profesor=request.user
    ).order_by("curso", "apellidos", "nombres")

    importaciones = RegistroImportacion.objects.filter(
        profesor=request.user
    ).order_by("-fecha_importacion")[:5]

    context = {
        "page_title": "Estudiantes",
        "estudiantes": estudiantes,
        "total_estudiantes": estudiantes.count(),
        "importaciones": importaciones,
    }
    return render(request, "students/student_list.html", context)


@login_required
def student_create(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save(commit=False)
            estudiante.profesor = request.user
            estudiante.save()
            messages.success(request, "Estudiante creado correctamente.")
            return redirect("students:list")
    else:
        form = EstudianteForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "titulo": "Nuevo estudiante",
            "modo": "crear",
        },
    )


@login_required
def student_update(request, pk):
    estudiante = get_object_or_404(
        Estudiante,
        pk=pk,
        profesor=request.user,
    )

    if request.method == "POST":
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, "Estudiante actualizado correctamente.")
            return redirect("students:list")
    else:
        form = EstudianteForm(instance=estudiante)

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "titulo": "Editar estudiante",
            "modo": "editar",
        },
    )


@login_required
def student_delete(request, pk):
    estudiante = get_object_or_404(
        Estudiante,
        pk=pk,
        profesor=request.user,
    )

    if request.method == "POST":
        estudiante.delete()
        messages.success(request, "Estudiante eliminado correctamente.")
        return redirect("students:list")

    return render(
        request,
        "students/student_delete.html",
        {
            "estudiante": estudiante,
        },
    )


@login_required
def student_import_csv(request):
    columnas_requeridas = [
        "nombres",
        "apellidos",
        "rut",
        "curso",
        "correo_apoderado",
        "telefono_apoderado",
        "observaciones",
    ]

    if request.method == "POST":
        form = CSVImportForm(request.POST, request.FILES)

        if form.is_valid():
            archivo = form.cleaned_data["archivo"]

            if not archivo.name.lower().endswith(".csv"):
                messages.error(request, "Debes subir un archivo con extensión .csv.")
                return redirect("students:import_csv")

            try:
                contenido = archivo.read().decode("utf-8-sig")
                csv_file = io.StringIO(contenido)
                reader = csv.DictReader(csv_file)

                if not reader.fieldnames:
                    messages.error(request, "El archivo CSV no contiene encabezados válidos.")
                    return redirect("students:import_csv")

                encabezados = [campo.strip() for campo in reader.fieldnames]

                columnas_faltantes = [
                    columna for columna in columnas_requeridas if columna not in encabezados
                ]

                if columnas_faltantes:
                    messages.error(
                        request,
                        "Faltan columnas obligatorias: " + ", ".join(columnas_faltantes)
                    )
                    return redirect("students:import_csv")

                total_registros = 0
                registros_exitosos = 0
                registros_error = 0

                for fila in reader:
                    total_registros += 1

                    nombres = (fila.get("nombres") or "").strip()
                    apellidos = (fila.get("apellidos") or "").strip()
                    rut = (fila.get("rut") or "").strip()
                    curso = (fila.get("curso") or "").strip()
                    correo_apoderado = (fila.get("correo_apoderado") or "").strip()
                    telefono_apoderado = (fila.get("telefono_apoderado") or "").strip()
                    observaciones = (fila.get("observaciones") or "").strip()

                    if not nombres or not apellidos or not curso:
                        registros_error += 1
                        continue

                    existe = Estudiante.objects.filter(
                        profesor=request.user,
                        nombres__iexact=nombres,
                        apellidos__iexact=apellidos,
                        curso__iexact=curso,
                        rut__iexact=rut,
                    ).exists()

                    if existe:
                        registros_error += 1
                        continue

                    Estudiante.objects.create(
                        profesor=request.user,
                        nombres=nombres,
                        apellidos=apellidos,
                        rut=rut,
                        curso=curso,
                        correo_apoderado=correo_apoderado,
                        telefono_apoderado=telefono_apoderado,
                        observaciones=observaciones,
                        activo=True,
                    )
                    registros_exitosos += 1

                RegistroImportacion.objects.create(
                    profesor=request.user,
                    nombre_archivo=archivo.name,
                    total_registros=total_registros,
                    registros_exitosos=registros_exitosos,
                    registros_error=registros_error,
                )

                messages.success(
                    request,
                    f"Importación finalizada. Total: {total_registros}, "
                    f"exitosos: {registros_exitosos}, con error: {registros_error}."
                )
                return redirect("students:list")

            except UnicodeDecodeError:
                messages.error(
                    request,
                    "No se pudo leer el archivo. Guárdalo en formato CSV UTF-8."
                )
                return redirect("students:import_csv")
    else:
        form = CSVImportForm()

    return render(
        request,
        "students/student_import.html",
        {
            "form": form,
            "columnas_requeridas": columnas_requeridas,
        },
    )