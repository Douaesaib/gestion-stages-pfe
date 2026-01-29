# Create your views here.
from django.shortcuts import render
from .models import Offre

def offres_list(request):
    offres = Offre.objects.select_related("entreprise").all().order_by("-id")
    return render(request, "stages/offres_list.html", {"offres": offres})
