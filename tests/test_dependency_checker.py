from resources import Inventory, Commentator, Seller, check_dependencies

def test_check_dependencies():
    # Crear inventario
    inventory = Inventory()
    inventory.add_item("microphone", 2)
    inventory.add_item("Products", 10)

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

# Ejecutar prueba
if __name__ == "__main__":
    test_check_dependencies()