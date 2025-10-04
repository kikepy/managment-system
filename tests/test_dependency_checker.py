from resources import *
def test_check_dependencies():
    # Crear inventario
    inventory = Inventory()
    inventory.add_item(Item("microphone", 0), 2)  # Pass item and quantity separately
    inventory.add_item(Item("Snacks", 0), 50)    # Pass item and quantity separately

    # Crear staff
    staff_list = [
        Commentator("John", ["English", "Spanish"], 5),
        Seller("Alice", 3, ["Snacks", "Drinks"])
    ]

    # Verificar dependencias
    if check_dependencies(staff_list, inventory):
        print("All dependencies are met. The event can proceed.")
    else:
        print("Dependencies are missing. The event cannot proceed.")