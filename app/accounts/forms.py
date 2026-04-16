from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control custom-input",
                "placeholder": "Ingresa tu usuario",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control custom-input",
                "placeholder": "Ingresa tu contraseña",
            }
        ),
    )