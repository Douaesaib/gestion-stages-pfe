from django.urls import path
from . import views

app_name = "stages"

urlpatterns = [
    path("offres/", views.offres_list, name="offres_list"),
]
