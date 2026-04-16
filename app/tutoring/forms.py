from django import forms

from students.models import Estudiante

from .models import EntrevistaTutoria


def contar_palabras(texto):
    return len([p for p in texto.strip().split() if p])


class EntrevistaTutoriaForm(forms.ModelForm):
    class Meta:
        model = EntrevistaTutoria
        exclude = ["profesor"]
        widgets = {
            "estudiante": forms.Select(attrs={"class": "form-select custom-input"}),
            "fecha": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control custom-input",
                }
            ),
            "fase_motivacional_dominante": forms.Select(
                attrs={"class": "form-select custom-input"}
            ),
            "situacion_trabajada": forms.Textarea(
                attrs={
                    "class": "form-control custom-input",
                    "rows": 2,
                    "placeholder": "Máximo 25 palabras.",
                }
            ),
            "desarrollo_sesion": forms.Textarea(
                attrs={
                    "class": "form-control custom-input",
                    "rows": 4,
                    "placeholder": "Máximo 100 palabras.",
                }
            ),
            "meta_concreta": forms.Textarea(
                attrs={
                    "class": "form-control custom-input",
                    "rows": 2,
                    "placeholder": "Máximo 30 palabras.",
                }
            ),
            "compromiso_tutor": forms.Textarea(
                attrs={
                    "class": "form-control custom-input",
                    "rows": 2,
                    "placeholder": "Máximo 30 palabras.",
                }
            ),
            "criterio_profesional": forms.RadioSelect(),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control custom-input",
                    "rows": 2,
                    "placeholder": "Máximo 40 palabras.",
                }
            ),
            "dimension_academica": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "dimension_socioemocional": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "dimension_identitaria": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "dimension_vincular": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "dimension_proyeccion": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        profesor = kwargs.pop("profesor", None)
        super().__init__(*args, **kwargs)

        if profesor is not None:
            self.fields["estudiante"].queryset = Estudiante.objects.filter(
                profesor=profesor
            ).order_by("curso", "apellidos", "nombres")
        else:
            self.fields["estudiante"].queryset = Estudiante.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        dimensiones = [
            cleaned_data.get("dimension_academica"),
            cleaned_data.get("dimension_socioemocional"),
            cleaned_data.get("dimension_identitaria"),
            cleaned_data.get("dimension_vincular"),
            cleaned_data.get("dimension_proyeccion"),
        ]

        seleccionadas = sum(1 for d in dimensiones if d)

        if seleccionadas == 0:
            raise forms.ValidationError("Debes seleccionar al menos una dimensión.")

        if seleccionadas > 3:
            raise forms.ValidationError("Solo puedes seleccionar máximo 3 dimensiones.")

        campos_palabras = {
            "situacion_trabajada": 25,
            "desarrollo_sesion": 100,
            "meta_concreta": 30,
            "compromiso_tutor": 30,
            "observaciones": 40,
        }

        for campo, max_palabras in campos_palabras.items():
            texto = cleaned_data.get(campo)
            if texto and contar_palabras(texto) > max_palabras:
                self.add_error(campo, f"Máximo {max_palabras} palabras.")

        return cleaned_data