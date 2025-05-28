import click
from ..models import Item, Session 

@click.group()
def item():
    """Manage grocery items"""
    pass

@item.command()
@click.argument('name')
@click.argument('category')
def add(name, category):
    """Add a new grocery item"""
    session = Session()
    new_item = Item(name=name, category=category)
    session.add(new_item)
    session.commit()
    click.echo(f" Added: {name} ({category})")

@item.command()
def list():
    """Show all items"""
    session = Session()
    items = session.query(Item).all()
    for item in items:
        click.echo(f"{item.id}: {item.name} ({item.category})")