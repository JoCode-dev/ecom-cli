import os.path
from datetime import datetime

import click
import pandas as pd


@click.command()
@click.argument("file_name", type=str)
def create_csv(file_name: str) -> None:
    files_directory = "cli"
    file_path = os.path.join(files_directory, file_name)

    """ Check if the file exists """
    if os.path.exists(file_path):
        if not file_path.endswith(".xlsx"):
            click.echo(f"{file_path} is not a .xlsx file")
            exit(1)

        df = pd.read_excel(file_path, engine="openpyxl")
        columns_for_contact = ["Nom complet", "Telephone"]
        df_contacts = df[columns_for_contact]

        """ Create an CSV file for contacts """
        today = datetime.now().strftime('%Y-%m-%d')
        contacts_file_name = f"contacts-{today}.csv"
        df_contacts.to_csv(f"{files_directory}/{contacts_file_name}",
                           index=False,
                           encoding="utf-8",
                           sep=",")

        click.echo(f"{file_path} is created")

    else:
        click.echo(f"File does not exist: {file_path}")
        exit(1)


@click.command()
@click.argument("file_name", type=str)
def create_delivery_card(file_name: str) -> None:
    pass
