from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from students.models import Estudiante
from .forms import EntrevistaTutoriaForm
from .models import EntrevistaTutoria


@login_required
def interview_list(request, student_id):
    estudiante = get_object_or_404(
        Estudiante,
        id=student_id,
        profesor=request.user,
    )

    entrevistas = EntrevistaTutoria.objects.filter(
        estudiante=estudiante,
        profesor=request.user,
    ).order_by("-fecha", "-fecha_creacion")

    return render(
        request,
        "tutoring/interview_list.html",
        {
            "estudiante": estudiante,
            "entrevistas": entrevistas,
        },
    )


@login_required
def interview_create(request):
    estudiante_inicial = None
    student_id = request.GET.get("student")

    if student_id:
        estudiante_inicial = Estudiante.objects.filter(
            id=student_id,
            profesor=request.user,
        ).first()

    if request.method == "POST":
        form = EntrevistaTutoriaForm(request.POST, profesor=request.user)
        if form.is_valid():
            entrevista = form.save(commit=False)
            entrevista.profesor = request.user
            entrevista.save()

            messages.success(request, "Registro guardado correctamente.")
            return redirect(
                "tutoring:list",
                student_id=entrevista.estudiante.id,
            )
    else:
        initial = {}
        if estudiante_inicial:
            initial["estudiante"] = estudiante_inicial

        form = EntrevistaTutoriaForm(
            profesor=request.user,
            initial=initial,
        )

    return render(
        request,
        "tutoring/interview_form.html",
        {
            "form": form,
        },
    )


@login_required
def interview_update(request, pk):
    entrevista = get_object_or_404(
        EntrevistaTutoria,
        id=pk,
        profesor=request.user,
    )

    if request.method == "POST":
        form = EntrevistaTutoriaForm(request.POST, instance=entrevista, profesor=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tutoría actualizada correctamente.")
            return redirect("tutoring:list", student_id=entrevista.estudiante.id)
    else:
        form = EntrevistaTutoriaForm(instance=entrevista, profesor=request.user)

    return render(
        request,
        "tutoring/interview_form.html",
        {
            "form": form,
            "titulo": "Editar tutoría",
            "estudiante": entrevista.estudiante,
        },
    )


@login_required
def interview_delete(request, pk):
    entrevista = get_object_or_404(
        EntrevistaTutoria,
        id=pk,
        profesor=request.user,
    )

    if request.method == "POST":
        student_id = entrevista.estudiante.id
        entrevista.delete()
        messages.success(request, "Registro eliminado.")
        return redirect("tutoring:list", student_id=student_id)

    return render(
        request,
        "tutoring/interview_delete.html",
        {"entrevista": entrevista},
    )