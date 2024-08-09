from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # CRUD methods
    path("create/", views.create, name="create"),
]
