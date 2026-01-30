from django.contrib import admin
from django.urls import path, include
from stages.views import offres_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", offres_list, name="home"),
    path("", include("stages.urls")),
]
