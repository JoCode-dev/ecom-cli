import click
import pandas as pd
import os.path
import pywhatkit as pwk
from keyboard import press
import subprocess


def send(numero: str, message: str):
    try:
        pwk.sendwhatmsg_instantly(
            phone_no=f"+{numero}",
            message=message
        )

        # Set browser to active window
        app_path = "/Applications/Firefox\ Developer\ Edition.app"
        cmd = f"open -a {app_path}"
        subprocess.call(cmd, shell=True)

        # Automatically press keyboard `Enter` key
        press("enter")
        return 'Succès'
    except Exception as e:
        return f'Erreur: {str(e)}'


def send_confirmation(numero: str, product: str, qte: str, total: str):
    confirmation_message = f"""
    *Confirmation de votre commande 🛒*

Bonjour cher client(e),
Merci pour votre commande chez AKWABA Store ! 🎉

🛍 Détail de votre commande :
• Produit : {product}
• Quantité : {qte}
• Total : {total}
• Mode de paiement : Paiement à la livraison

📦 Votre commande sera expédiée sous *24h* . Vous recevrez un message dès qu’elle sera en route.

Merci pour votre confiance et à bientôt ! 😊
    """

    send(numero, confirmation_message)


def send_after_sales_support_message(numero: str, product: str, ):
    message = f"""
*Suivi après-vente 🛍*
*Tout s’est bien passé ? 😊*

Bonjour cher client(e),
Nous espérons que vous êtes satisfait(e) de votre achat chez AKWABA Store !

📦 Produit : {product}
👉 Besoin d’aide ou de conseils ? Répondez directement à ce message, nous sommes là pour vous.

Merci encore pour votre confiance, et à bientôt !

AKWABA Store – Votre satisfaction est notre priorité. 🌟"""
    send(numero, message)


@click.command()
@click.argument("file_name", type=str)
@click.option("--tag", type=str, help="Type of action [confirmation]", required=True)
def send_messages(file_name: str, tag: str) -> None:
    files_directory = "cli"

    file_path = os.path.join(files_directory, file_name)

    """ Check if the file exists """
    if os.path.exists(file_path):
        df = pd.read_excel(file_path, engine="openpyxl")
        if "Telephone" not in df.columns:
            click.echo("La colonne 'Telephone' est absente du fichier.")
            exit(1)

        def send_wrapper(row):
            numero = row["Telephone"]
            product = row["Produit"]
            qte = row["Quantite"]
            total = row["Prix total"]

            if tag == "confirmation":
                return send_confirmation(numero, product=product, qte=qte, total=total)

            if tag == "suivis-apres-vente":
                return send_after_sales_support_message(numero, product=product)

        df['statut_envoi'] = df.apply(send_wrapper, axis=1)
        print(df[['Telephone', 'statut_envoi']])

    else:
        click.echo(f"File does not exist: {file_path}")
    exit(1)
