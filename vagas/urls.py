from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:vaga_id>/', views.vaga, name='vaga'),
    # CRUD methods
    path("vagas/", views.vagas, name="vagas"),
    path("create/", views.create, name="create"),
    # Login
    path('user/create/', views.register, name='register'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
    path('user/update/', views.user_update, name='user_update'),
]
