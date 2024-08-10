from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # CRUD methods
    path("vagas/", views.vagas, name="vagas"),
    path("create/", views.create, name="create"),
]
