import click

from .functions.files import create_csv
from .functions.whatsapp import send_messages

@click.group()
def cli() -> None:
    print("Hello JoCode!")

cli.add_command(create_csv)
cli.add_command(send_messages)