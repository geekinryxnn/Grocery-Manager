import click
from ..models import GroceryList, Item, ListItem, Session

def show_menu():
    click.echo("\n Grocery List Manager")
    click.echo("1. Create new list")
    click.echo("2. Add items to list")
    click.echo("3. View all lists")
    click.echo("4. Show list contents")
    click.echo("5. Remove item from list")
    click.echo("6. Delete a list")
    click.echo("0. Exit")

@click.group(invoke_without_command=True)
@click.pass_context
def glist(ctx):
    """Manage grocery lists with numeric menu"""
    if ctx.invoked_subcommand is None:
        while True:
            show_menu()
            choice = click.prompt("Enter your choice", type=int)
            
            if choice == 0:
                break
            elif choice == 1:
                create_list()
            elif choice == 2:
                add_items()
            elif choice == 3:
                list_all_lists()
            elif choice == 4:
                show_list_contents()
            elif choice == 5:
                remove_item()
            elif choice == 6:
                delete_list()
            else:
                click.echo("Invalid choice, try again")

def create_list():
    """Create new list"""
    name = click.prompt("Enter list name")
    with Session() as session:
        session.add(GroceryList(name=name))
        session.commit()
        click.echo(f"Created: {name}")

def add_items():
    """Add items to list"""
    with Session() as session:
        lists = session.query(GroceryList).all()
        click.echo("\nAvailable lists:")
        for lst in lists:
            click.echo(f"{lst.id}. {lst.name}")
        list_id = click.prompt("Select list ID", type=int)
        
        items = session.query(Item).all()
        click.echo("\nAvailable items:")
        for item in items:
            click.echo(f"{item.id}. {item.name} ({item.category})")
        item_id = click.prompt("Select item ID", type=int)
        
        if session.query(ListItem).filter_by(list_id=list_id, item_id=item_id).first():
            click.echo("Item already in list")
            return
        
        session.add(ListItem(list_id=list_id, item_id=item_id))
        session.commit()
        click.echo("Item added to list")

def list_all_lists():
    """Show all lists"""
    with Session() as session:
        lists = session.query(GroceryList).all()
        if not lists:
            click.echo("No lists found")
            return
        click.echo("\n Your Lists:")
        for lst in lists:
            click.echo(f"{lst.id}. {lst.name}")

def show_list_contents():
    """Show list contents"""
    list_id = click.prompt("Enter list ID to view", type=int)
    with Session() as session:
        lst = session.query(GroceryList).get(list_id)
        if not lst:
            click.echo("List not found")
            return
        
        items = session.query(Item).join(ListItem).filter(
            ListItem.list_id == list_id).all()
        
        click.echo(f"\n{lst.name}:")
        for item in items:
            click.echo(f"  - {item.name} ({item.category})")

def remove_item():
    """Remove item from list"""
    list_id = click.prompt("Enter list ID", type=int)
    with Session() as session:
        items = session.query(Item).join(ListItem).filter(
            ListItem.list_id == list_id).all()
        
        if not items:
            click.echo("No items in this list")
            return
        
        click.echo("\n Items in list:")
        for item in items:
            click.echo(f"{item.id}. {item.name}")
        
        item_id = click.prompt("Enter item ID to remove", type=int)
        if not session.query(ListItem).filter_by(
            list_id=list_id, item_id=item_id
        ).delete():
            click.echo("Item not found in list")
            return
        
        session.commit()
        click.echo("Item removed")

def delete_list():
    """Delete a list and its items"""
    with Session() as session:
        lists = session.query(GroceryList).all()
        if not lists:
            click.echo("No lists available to delete")
            return
        
        click.echo("\n Available lists:")
        for lst in lists:
            click.echo(f"{lst.id}. {lst.name}")
        
        list_id = click.prompt("Enter list ID to delete", type=int)
        lst = session.query(GroceryList).get(list_id)
        
        if not lst:
            click.echo("List not found")
            return
        
        if click.confirm(f"Delete '{lst.name}' and all its items?"):
            session.query(ListItem).filter_by(list_id=list_id).delete()
            session.delete(lst)
            session.commit()
            click.echo(f"Deleted list: {lst.name}")
        else:
            click.echo("Deletion cancelled")

def handle_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
    return wrapper


for cmd in [create_list, add_items, list_all_lists, show_list_contents, 
            remove_item, delete_list]:
    cmd = handle_errors(cmd)