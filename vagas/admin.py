from django.contrib import admin
from vagas import models

# Register your models here.

@admin.register(models.Vaga)
class VagaAdmin(admin.ModelAdmin):
    ...