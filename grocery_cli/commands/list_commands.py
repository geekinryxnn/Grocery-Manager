import click
from ..models import GroceryList, Item, ListItem, Session

def show_menu():
    print("Grocery List Manager")
    print("1. Create new list")
    print("2. Add item to list")
    print("3. View all lists")
    print("4. Show list contents")
    print("5. Remove item from list")
    print("6. Delete a list")
    print("0. Exit")

def get_lists():
    with Session() as session:
        return session.query(GroceryList).all()

def get_int(prompt):
    while True:
        try:
            return int(click.prompt(prompt))
        except ValueError as e:
            print(f"Error: \"{e.args[0]}\" is not a valid integer.")

@click.command()
def glist():
    """Manage lists"""
    while True:
        show_menu()
        choice = get_int("Enter choice")
        print()
        if choice == 0:
            break
        elif choice == 1:
            new_list()
        elif choice == 2:
            add_item()
        elif choice == 3:
            show_lists()
        elif choice == 4:
            show_items()
        elif choice == 5:
            remove_item()
        elif choice == 6:
            delete_list()
        else:
            print("Bad choice")
        print()

def new_list():
    name = click.prompt("Name")
    with Session() as session:
        session.add(GroceryList(name=name))
        session.commit()
        print(f"Added: {name}")

def add_item():
    lists = get_lists()
    if not lists:
        print("No lists")
        return
    i = 1
    for lst in lists:
        print(f"{i}. {lst.name}")
        i += 1
    num = get_int("List number")
    if not 1 <= num <= len(lists):
        print("Bad list")
        return
    lst = lists[num - 1]
    
    name = click.prompt("Item")
    with Session() as session:
        item = session.query(Item).filter(Item.name.ilike(name)).first()
        if not item:
            item = Item(name=name, category="General")
            session.add(item)
            session.commit()
        
        if session.query(ListItem).filter_by(list_id=lst.id, item_id=item.id).first():
            print(f"'{name}' already in '{lst.name}'")
            return
        
        session.add(ListItem(list_id=lst.id, item_id=item.id))
        session.commit()
        print(f"Item '{name}' added")

def show_lists():
    lists = get_lists()
    if not lists:
        print("No lists")
        return
    print("Lists:")
    i = 1
    for lst in lists:
        print(f"{i}. {lst.name}")
        i += 1

def show_items():
    lists = get_lists()
    if not lists:
        print("No lists")
        return
    i = 1
    for lst in lists:
        print(f"{i}. {lst.name}")
        i += 1
    num = get_int("List number")
    print()
    if not 1 <= num <= len(lists):
        print("Bad list")
        return
    lst = lists[num - 1]
    
    with Session() as session:
        items = session.query(Item).join(ListItem).filter(ListItem.list_id == lst.id).all()
        print(f"{lst.name}:")
        if not items:
            print("  Empty")
        for item in items:
            print(f"  - {item.name} ({item.category})")

def remove_item():
    lists = get_lists()
    if not lists:
        print("No lists")
        return
    i = 1
    for lst in lists:
        print(f"{i}. {lst.name}")
        i += 1
    num = get_int("List number")
    if not 1 <= num <= len(lists):
        print("Bad list")
        return
    lst = lists[num - 1]
    
    with Session() as session:
        items = session.query(Item).join(ListItem).filter(ListItem.list_id == lst.id).all()
        if not items:
            print("No items")
            return
        i = 1
        for item in items:
            print(f"{i}. {item.name}")
            i += 1
        item_num = get_int("Item number")
        if not 1 <= item_num <= len(items):
            print("Bad item")
            return
        
        item = items[item_num - 1]
        session.query(ListItem).filter_by(list_id=lst.id, item_id=item.id).delete()
        session.commit()
        print("Item gone")

def delete_list():
    lists = get_lists()
    if not lists:
        print("No lists")
        return
    i = 1
    for lst in lists:
        print(f"{i}. {lst.name}")
        i += 1
    num = get_int("List number to delete")
    if not 1 <= num <= len(lists):
        print("Bad list")
        return
    lst = lists[num - 1]
    
    with Session() as session:
        session.query(ListItem).filter_by(list_id=lst.id).delete()
        session.delete(lst)
        session.commit()
        print(f"Deleted {lst.name}")
