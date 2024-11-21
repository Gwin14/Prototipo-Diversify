from . import models
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


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


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label="E-mail")
    cpf = forms.CharField(required=True, label="CPF", max_length=14)
    CID = forms.CharField(required=True, label="CID", max_length=50)
    phone_number = forms.CharField(required=True, label="Telefone", max_length=15)
    address = forms.CharField(required=True, label="Endereço", widget=forms.Textarea)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
            "cpf",
            "CID",
            "phone_number",
            "address",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Já existe um usuário com este e-mail.", code="invalid"
            )
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        # Adicione aqui uma validação de CPF (por exemplo, usando um regex ou biblioteca)
        return cpf


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2, max_length=30, required=True, label="Nome"
    )
    last_name = forms.CharField(
        min_length=2, max_length=30, required=True, label="Sobrenome"
    )
    email = forms.EmailField(required=True, label="E-mail")
    cpf = forms.CharField(required=True, label="CPF", max_length=14)
    CID = forms.CharField(required=True, label="CID", max_length=50)
    phone_number = forms.CharField(required=True, label="Telefone", max_length=15)
    address = forms.CharField(required=True, label="Endereço", widget=forms.Textarea)

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
    )
    password2 = forms.CharField(
        label="Confirme a senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "cpf",
            "CID",
            "phone_number",
            "address",
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", ValidationError("As senhas não coincidem."))
        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    "email",
                    ValidationError(
                        "Já existe um usuário com este e-mail.", code="invalid"
                    ),
                )
        return email
