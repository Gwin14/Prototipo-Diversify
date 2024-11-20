from django.contrib import admin
from django.urls import include, path
from vagas import urls

urlpatterns = [
    path("", include(urls)),
    path("admin/", admin.site.urls),
]
