import click
from .commands.item_commands import item
from .commands.list_commands import glist
from .models.base import init_db

@click.group()
def cli():
    """Grocery List Manager CLI"""
    pass

cli.add_command(item)
cli.add_command(glist)

if __name__ == '__main__':
    init_db()
    cli()