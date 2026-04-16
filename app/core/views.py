from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    context = {
        "page_title": "Inicio",
    }
    return render(request, "core/home.html", context)


@login_required
def dashboard(request):
    context = {
        "page_title": "Panel principal",
        "total_estudiantes": request.user.estudiantes.count(),
        "total_importaciones": request.user.importaciones.count(),
    }
    return render(request, "core/dashboard.html", context)