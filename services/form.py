from django import forms

from services.enums import Phase


class FilterForm(forms.Form):
    phase = forms.ChoiceField(
        label="Maturité",
        choices=[("", "Selectionner une option")] + Phase.choices,
        widget=forms.Select(
            attrs={
                "class": "fr-select",
                "onchange": "this.form.submit()",
            }
        ),
    )
