import click
import pandas as pd
import os.path
import pywhatkit as pwk


def send(numero: str):
    try:
        pwk.sendwhatmsg_instantly(
            phone_no=f"+{numero}",
            message="Hello"
        )
        return 'Succès'
    except Exception as e:
        return f'Erreur: {str(e)}'


@click.command()
@click.argument("file_name", type=str)
def send_messages(file_name) -> None:
    files_directory = "cli"

    file_path = os.path.join(files_directory, file_name)

    """ Check if the file exists """
    if os.path.exists(file_path):
        df = pd.read_excel(file_path, engine="openpyxl")
        telephones = df["Telephone"]
        print(telephones)
        df['statut_envoi'] = telephones.apply(send)
        print(df[['Telephone', 'statut_envoi']])

    else:
        click.echo(f"File does not exist: {file_path}")
        exit(1)
