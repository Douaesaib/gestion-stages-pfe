from django.contrib import admin
from django.urls import path
from stages.views import offres_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", offres_list, name="home"),      #  الصفحة الرئيسية
    path("offres/", offres_list, name="offres_list"),
]
