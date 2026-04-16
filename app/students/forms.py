from django import forms

from .models import Estudiante


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = [
            "nombres",
            "apellidos",
            "rut",
            "curso",
            "correo_apoderado",
            "telefono_apoderado",
            "observaciones",
            "activo",
        ]
        widgets = {
            "nombres": forms.TextInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Nombres del estudiante",
                }
            ),
            "apellidos": forms.TextInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Apellidos del estudiante",
                }
            ),
            "rut": forms.TextInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "RUT",
                }
            ),
            "curso": forms.TextInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Curso",
                }
            ),
            "correo_apoderado": forms.EmailInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Correo del apoderado",
                }
            ),
            "telefono_apoderado": forms.TextInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Teléfono del apoderado",
                }
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control custom-input",
                    "rows": 4,
                    "placeholder": "Observaciones",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class CSVImportForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo CSV",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control custom-input",
                "accept": ".csv",
            }
        ),
    )