from . import models
from django import forms


class VagasForm(forms.ModelForm):
    class Meta:
        model = models.Vaga
        fields = (
            "title",
            "description",
            "salary",
            "experience_years",
            "location",
            "company_name",
            "company_description",
            "company_website",
            "tags",
        )
