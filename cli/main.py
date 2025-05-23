import click

from .functions.files import create_csv
from .functions.whatsapp import send_messages
from .functions.delivery import create_delivery_card


@click.group()
def cli() -> None:
    print("Hello JoCode!")


cli.add_command(create_csv)
cli.add_command(send_messages)
cli.add_command(create_delivery_card)
