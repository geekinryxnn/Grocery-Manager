import click
from ..models import GroceryList, Item, ListItem, Session

def show_menu():
    menu = """Grocery List Manager
1. Create new list
2. Add item to list
3. View all lists
4. Show list contents
5. Remove item from list
6. Delete a list
0. Exit"""
    print(menu)

def get_lists():
    with Session() as session:
        return session.query(GroceryList).all()

def get_int(prompt):
    while True:
        try:
            return int(click.prompt(prompt))
        except ValueError as e:
            print(f"Error: \"{e.args[0]}\" is not a valid integer.")

def select_list(lists, prompt="List number"):
    for i, lst in enumerate(lists, 1):
        print(f"{i}. {lst.name}")
    num = get_int(prompt)
    return lists[num - 1] if 1 <= num <= len(lists) else None

@click.command()
def glist():
    """Manage lists"""
    while True:
        show_menu()
        choice = get_int("Enter choice")
        print()
        if choice == 0:
            break
        actions = {
            1: new_list,
            2: add_item,
            3: show_lists,
            4: show_items,
            5: remove_item,
            6: delete_list
        }
        actions.get(choice, lambda: print("Bad choice"))()
        print()

def new_list():
    name = click.prompt("Name")
    with Session() as session:
        session.add(GroceryList(name=name))
        session.commit()
        print(f"Added: {name}")

def add_item():
    if not (lists := get_lists()):
        return print("No lists")
    if not (lst := select_list(lists)):
        return print("Bad list")
    
    name = click.prompt("Item")
    with Session() as session:
        item = session.query(Item).filter(Item.name.ilike(name)).first()
        if not item:
            item = Item(name=name, category="General")
            session.add(item)
            session.commit()
        
        if session.query(ListItem).filter_by(list_id=lst.id, item_id=item.id).first():
            return print(f"'{name}' already in '{lst.name}'")
        
        session.add(ListItem(list_id=lst.id, item_id=item.id))
        session.commit()
        print(f"Item '{name}' added")

def show_lists():
    if not (lists := get_lists()):
        return print("No lists")
    print("Lists:")
    for i, lst in enumerate(lists, 1):
        print(f"{i}. {lst.name}")

def show_items():
    if not (lists := get_lists()):
        return print("No lists")
    if not (lst := select_list(lists)):
        return print("Bad list")
    
    with Session() as session:
        items = session.query(Item).join(ListItem).filter(ListItem.list_id == lst.id).all()
        print(f"{lst.name}:")
        print("  Empty" if not items else "\n".join(f"  - {i.name} ({i.category})" for i in items))

def remove_item():
    if not (lists := get_lists()):
        return print("No lists")
    if not (lst := select_list(lists)):
        return print("Bad list")
    
    with Session() as session:
        items = session.query(Item).join(ListItem).filter(ListItem.list_id == lst.id).all()
        if not items:
            return print("No items")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item.name}")
        if not (1 <= (item_num := get_int("Item number")) <= len(items)):
            return print("Bad item")
        
        item = items[item_num - 1]
        session.query(ListItem).filter_by(list_id=lst.id, item_id=item.id).delete()
        session.commit()
        print("Item gone")

def delete_list():
    if not (lists := get_lists()):
        return print("No lists")
    if not (lst := select_list(lists, "List number to delete")):
        return print("Bad list")
    
    with Session() as session:
        session.query(ListItem).filter_by(list_id=lst.id).delete()
        session.delete(lst)
        session.commit()
        print(f"Deleted {lst.name}")
