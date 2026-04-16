from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from .forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Bienvenido, {form.get_user().username}."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Usuario o contraseña incorrectos."
        )
        return super().form_invalid(form)


def custom_logout_view(request):
    logout(request)
    messages.success(
        request,
        "Te has deslogueado con éxito."
    )
    return redirect("core:home")