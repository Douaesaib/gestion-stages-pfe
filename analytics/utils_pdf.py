from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def generer_pdf_convention():
    # 1. Créer le tampon mémoire (comme un fichier virtuel)
    buffer = BytesIO()
    
    # 2. Créer le document PDF
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # 3. Dessiner dessus (x, y) - Attention le (0,0) est en bas à gauche
    p.setFont("Helvetica-Bold", 20)
    p.drawString(200, 800, "CONVENTION DE STAGE")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, "Entre le stagiaire : DOUAE SAIB (Exemple)")
    p.drawString(50, 730, "Et l'entreprise : GOOGLE MAROC (Exemple)")
    p.drawString(50, 700, "Article 1 : Le stage débutera le 01/02/2026...")
    
    # 4. Fermer et sauvegarder
    p.showPage()
    p.save()
    
    # 5. Renvoyer le fichier au navigateur
    buffer.seek(0)
    return buffer