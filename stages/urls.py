from django.urls import path
from . import views

app_name = "stages"

urlpatterns = [
    path("offres/", views.offres_list, name="offres_list"),
    path("offres/<int:offre_id>/postuler/", views.postuler, name="postuler"),
]
