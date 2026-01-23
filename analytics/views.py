from django.shortcuts import render
from .utils_pdf import generer_pdf_convention
from django.http import FileResponse
def dashboard_view(request):
    #en remplace plus tard par Stagiaire.objects.count()
    context = {
        'nb_stagiaires': 142,
        'nb_entreprise': 35,
        'nb_offres': 12,
        'nb_convention': 98,
    }
    return render(request, 'analytics/dashboard.html', context)
def download_convention(request):
    buffer = generer_pdf_convention()
    return FileResponse(buffer, as_attachment=True, filename='convention_stage.pdf')
