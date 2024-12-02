from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("vaga/<int:vaga_id>/", views.detalhe_vaga, name="vaga"),
    path("search/", views.search, name="search"),
    # CRUD methods
    path("vagas/", views.vagas, name="vagas"),
    path("create/", views.create, name="create"),
    path("delete/<int:vaga_id>/", views.delete, name="delete"),
    # Login
    path("user/create/", views.register, name="register"),
    path("user/login/", views.login_view, name="login"),
    path("user/logout/", views.logout_view, name="logout"),
    path("user/update/", views.user_update, name="user_update"),



]
