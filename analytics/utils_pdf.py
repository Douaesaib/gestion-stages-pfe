from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, blue, gray
from reportlab.lib.units import cm
from django.conf import settings
import os

def generer_pdf_convention(stagiaire_nom="ETUDIANT INCONNU", entreprise_nom="ENTREPRISE NON SPECIFIEE"):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- 1. EN-TÊTE (Header) ---
    logo_path = os.path.join(settings.BASE_DIR, 'analytics', 'images', 'logo_fac.jpg')
    
    if os.path.exists(logo_path):
        # Qbel kant (height - 3.5), db rddinaha (height - 5.0) bash yhbet
        p.drawImage(logo_path, 1.5 * cm, height - 7.5 * cm, width=2.5*cm, preserveAspectRatio=True, mask='auto')

    # Titre de l'Université (Centré)
    p.setFillColor(black)
    p.setFont("Helvetica-Bold", 14)
    # Hna kan-l3bu b l'rtifa3 (height - X) bash nqadu l'ktaba
    p.drawCentredString(width / 2, height - 3.0 * cm, "ROYAUME DU MAROC")
    
    p.setFont("Helvetica", 11)
    p.drawCentredString(width / 2, height - 3.6 * cm, "Université Abdelmalek Essaâdi")
    p.drawCentredString(width / 2, height - 4.2 * cm, "Faculté des Sciences - Tétouan")

    # Ligne de séparation (Zrqqa) - Hta hiya hbbtha bash tji taht l'logo
    p.setLineWidth(1)
    p.setStrokeColor(blue)
    p.line(1.5 * cm, height - 5.5 * cm, width - 1.5 * cm, height - 5.5 * cm)

    # --- 2. TITRE PRINCIPAL ---
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(black)
    p.drawCentredString(width / 2, height - 7 * cm, "CONVENTION DE STAGE PFE")

    # --- 3. LE CORPS (Body) ---
    y_position = height - 10 * cm
    
    # Phrase d'intro
    p.setFont("Helvetica", 12)
    p.drawString(2.5 * cm, y_position, "Entre les soussignés :")
    y_position -= 1.5 * cm

    # PARTIE 1 : L'ETABLISSEMENT
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(blue)
    p.drawString(3 * cm, y_position, "1. L'Établissement : Faculté des Sciences de Tétouan")
    p.setFillColor(black)
    p.setFont("Helvetica", 11)
    p.drawString(3.5 * cm, y_position - 0.7 * cm, "Représenté par : Monsieur le Doyen")
    y_position -= 2.5 * cm

    # PARTIE 2 : L'ENTREPRISE (Dynamique)
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(blue)
    p.drawString(3 * cm, y_position, f"2. L'Entreprise d'Accueil : {entreprise_nom}")
    p.setFillColor(black)
    p.setFont("Helvetica", 11)
    p.drawString(3.5 * cm, y_position - 0.7 * cm, "Adresse : (Adresse de l'entreprise ici...)")
    p.drawString(3.5 * cm, y_position - 1.4 * cm, "Représentée par : (Nom du Responsable)")
    y_position -= 3.5 * cm

    # PARTIE 3 : LE STAGIAIRE (Dynamique)
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(blue)
    p.drawString(3 * cm, y_position, f"3. Le Stagiaire : {stagiaire_nom}")
    p.setFillColor(black)
    p.setFont("Helvetica", 11)
    p.drawString(3.5 * cm, y_position - 0.7 * cm, "Filière : Génie Informatique (Exemple)")
    p.drawString(3.5 * cm, y_position - 1.4 * cm, "Année Universitaire : 2025/2026")
    y_position -= 3 * cm

    # --- 4. SIGNATURES ---
    p.setLineWidth(0.5)
    p.setStrokeColor(gray)
    p.line(2 * cm, y_position, width - 2 * cm, y_position)
    y_position -= 1 * cm

    p.setFont("Helvetica-Bold", 10)
    p.drawString(2.5 * cm, y_position, "Signature du Stagiaire")
    p.drawString(8 * cm, y_position, "Signature de l'Entreprise")
    p.drawString(14.5 * cm, y_position, "Signature du Doyen")

    # --- FIN ---
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer