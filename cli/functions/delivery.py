import os
import pandas as pd
import click

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
from datetime import datetime


def wrap_text(text, canvas, font_name, font_size, max_width):
    """Fonction pour wrapper le texte si trop long"""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        line_width = canvas.stringWidth(' '.join(current_line), font_name, font_size)
        if line_width > max_width:
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []

    if current_line:
        lines.append(' '.join(current_line))

    return lines


@click.command()
@click.argument("file_name", type=str)
def create_delivery_card(file_name: str) -> None:
    files_directory = "cli"

    file_path = os.path.join(files_directory, file_name)

    """ Check if the file exists """
    if os.path.exists(file_path):
        df = pd.read_excel(file_path, engine="openpyxl")
        print(df.head())
        if "Telephone" not in df.columns:
            click.echo("La colonne 'Telephone' est absente du fichier.")
            exit(1)

            # Dimensions de la page en paysage
        width, height = landscape(letter)

        # Configuration des marges et espacements
        margin = 30  # marges de la page
        box_spacing = 15  # espacement entre les cases

        # Calcul des dimensions des cases (2 colonnes x 3 lignes)
        # Les cases prennent toute la largeur disponible
        box_width = (width - 2 * margin - box_spacing) / 2
        box_height = 130  # (height - 2 * margin - 2 * box_spacing) / 3

        # Création du PDF
        output_filename = f"Fiche de livraison-{datetime.today().strftime('%Y-%m-%d')}.pdf"
        c = canvas.Canvas(output_filename, pagesize=landscape(letter))

        # Calcul du nombre de pages nécessaires
        cards_per_page = 8
        total_pages = math.ceil(len(df) / cards_per_page)

        for page in range(total_pages):
            # Position initiale
            x = margin
            y = height - margin - box_height

            # Index de début pour cette page
            start_idx = page * cards_per_page

            # Traitement de 6 contacts par page
            for idx in range(start_idx, min(start_idx + cards_per_page, len(df))):
                # Dessiner le cadre
                c.rect(x, y, box_width, box_height)

                # Ajouter le contenu
                contact = df.iloc[idx]

                # Position du texte à l'intérieur de la case
                text_x = x + 10
                text_y = y + box_height - 20

                # Ajouter les informations du contact
                c.setFont("Helvetica-Bold", 12)
                c.drawString(text_x, text_y, f"{contact['Nom complet']}")

                c.setFont("Helvetica", 14)
                c.drawString(text_x, text_y - 20, f"Tél: {contact['Telephone']}")

                # Wrap l'adresse si elle est trop longue
                address_lines = wrap_text(str(contact['Adresse']), c, "Helvetica", 12, box_width - 100)

                # Ajouter les informations sur le produit
                c.setFont("Helvetica-Bold", 12)
                c.drawString(text_x, text_y - 70, f"Produit: {contact['Produit']} - Quantité: {contact['Quantite']}")

                # Ajouter le prix
                c.setFont("Helvetica-Bold", 18)
                c.drawString(text_x, text_y - 90, f"Prix: {contact['Prix total']} f")

                for i, line in enumerate(address_lines):
                    c.setFont("Helvetica-Bold", 13)
                    c.drawString(text_x, text_y - 40 - (i * 12), line)

                # Passer à la position suivante
                if x + box_width + box_spacing + box_width <= width:
                    x += box_width + box_spacing
                else:
                    x = margin
                    y -= box_height + box_spacing

            # Nouvelle page si nécessaire
            if page < total_pages - 1:
                c.showPage()

        # Sauvegarder le PDF
        c.save()

        print(f"File saved")
